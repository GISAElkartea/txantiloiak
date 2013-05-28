from __future__ import unicode_literals
import codecs
import os

from argparse import ArgumentParser
import jinja2
import yaml



class Environment(object):
    config_file_name = 'config.yaml'

    def __init__(self, extra_configs=None):
        self.extra_configs = extra_configs if extra_configs is not None else []

    def get_document(self, name):
        for document in self.documents:
            if document.name.lower() == name.lower():
                return document
        raise Exception('No document with such name')

    @property
    def documents(self):
        for config_path in self.extra_configs:
            yield Document(config_path)
        for dirpath, dirnames, filenames in os.walk('documents'):
            if self.config_file_name in filenames:
                config_path = os.path.join(dirpath, self.config_file_name)
                yield Document(config_path)


class Document(object):
    def __init__(self, config_file):
        self.base_dir = os.path.dirname(config_file)
        with open(config_file) as config:
            config = yaml.load(config)
        for key in 'name', 'templates', 'style', 'questionnaire':
            setattr(self, key, config.get(key))

    def __unicode__(self):
        return self.name

    @property
    def languages(self):
        return self.templates.keys()
        
    def get_template(self, language=None):
        if language is None:
            if len(self.languages) == 1:
                language = self.languages[0]
            else:
                raise Exception('Multiple possible languages, please select one')
        filename = os.path.join(self.base_dir, self.templates[language])
        with codecs.open(filename, encoding='utf-8') as template:
            return jinja2.Template(template.read())

    def ask_questionnaire(self):
        context = {}
        for key, details in self.questionnaire.items():
            default = details.get('default', '')

            question = details['question']
            if default:
                question = '{} [{}]: '.format(question, default)
            else:
                question = '{}: '.format(question)

            answer = ''
            while not answer:
                answer = raw_input(question) or default
            context[key] = answer
        return context

    def fill(self, language=None):
        template = self.get_template(language)
        context = self.ask_questionnaire()
        return template.render(**context)
        


class Command(object):
    def __init__(self):
        self.environment = Environment()
        self.parser = self.get_parser()

    def get_parser(self):
        parser = ArgumentParser(description='txantiloilak')
        subparsers = parser.add_subparsers()

        listing = subparsers.add_parser('list')
        listing.set_defaults(func=self.list_documents)

        filling = subparsers.add_parser('fill')
        filling.add_argument('document', metavar='NAME', type=str)
        filling.add_argument('-l', '--language', metavar='LANG', type=str)
        filling.add_argument('output', metavar='FILENAME', type=str)
        filling.set_defaults(func=self.fill)

        #rendering = subparsers.add_parser('render')

        return parser

    
    def list_documents(self, args):
        for document in self.environment.documents:
            print document.name
            print document.languages

    def fill(self, args):
        document = self.environment.get_document(args.document)
        data = document.fill(args.language)
        with codecs.open(args.output, 'w', encoding='utf-8') as output:
            output.write(data)

    def main(self):
        args = self.parser.parse_args()
        args.func(args)



if __name__ == '__main__':
    command = Command()
    command.main()
