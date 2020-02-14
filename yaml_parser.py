import yaml
from string import Template


def combine(terms, accum, res=[]):
    last = (len(terms) == 1)
    n = len(terms[0])
    for i in range(n):
        item = accum + terms[0][i]
        if last:
            res.append(item)
        else:
            combine(terms[1:], item, res)


def generate_alphas():

    with open("alpha.yaml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            f = open('alpha_template', 'r')
            dd = {'featureImport': '', 'featureList': '', 'featureInit': '', 'alphaName': ''}
            template = f.read()
            res = template.format(**dd)
            for alpha_name, alpha_properties in data.items():
                features = alpha_properties['Features']
                all_feature_names = []
                for feature_name, feature_properties in features.items():
                    name = feature_name.lower() + '_'
                    features = [ff for ff in feature_properties.values()]
                    print(features)
                    for i in range(len(features)):
                        for j in range(len(features[i])):
                            if i < len(features):
                                name += features[i+1][j]

                    break

        except yaml.YAMLError as exc:
            print(exc)

if __name__ == '__main__':
    #generate_alphas()
    a = [['ab', 'cd', 'ef'], ['12', '34', '56']]
    ss = []
    combine(a, '', res=ss)
    print(ss)
