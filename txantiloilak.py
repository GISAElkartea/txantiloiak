from __future__ import unicode_literals
import codecs

from argparse import ArgumentParser
from jinja2 import Environment, PackageLoader
import yaml


jinja_env = Environment(loader=PackageLoader('txantiloilak', 'templates'))


class Filler(object):
    def fill(self, name, language):
        template = self.get_template(name, language)
        context = self.ask_questionnaire(name)
        return template.render(**context)

    def ask_questionnaire(self, name):
        questionnaire = self.get_questionnaire(name)
        context = {}
        for key, details in questionnaire.items():
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

    def get_questionnaire(self, name):
        filename = 'questionnaires/{name}.yaml'.format(name=name)
        with open(filename) as questionnaire:
            return yaml.load(questionnaire)

    def get_template(self, name, language):
        filename = '{language}/{name}.rst'.format(
                name=name, language=language)
        return jinja_env.get_template(filename)
        

def get_parser():
    parser = ArgumentParser(description='txantiloilak')
    subparsers = parser.add_subparsers()

    filling = subparsers.add_parser('fill')
    filling.add_argument('template', metavar='NAME', type=str)
    filling.add_argument('language', metavar='LANG', type=str)
    filling.add_argument('output', metavar='FILENAME', type=str)

    rendering = subparsers.add_parser('render')

    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    filler = Filler()
    data = filler.fill('budget', 'eu')
    with codecs.open(args.output, 'w', encoding='utf-8') as output:
        output.write(data)



if __name__ == '__main__':
    main()
