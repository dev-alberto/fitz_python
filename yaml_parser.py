import yaml
import itertools
from data.factory_raw_data import Get_period_only_managers
import importlib
from feature.feature import EmptyFeature
import pandas as pd


def get_all_dict_combinations(dd):
    _keys = dd.keys()
    _values = (dd[key] for key in _keys)
    return [dict(zip(_keys, combination)) for combination in itertools.product(*_values)]


# given name and property dict, instantiate feature
def create_feature(name, dictionary):
    class_ = getattr(importlib.import_module("feature." + name.lower()), name)
    return class_(**dictionary)


def get_all_feature_combinations(feature_name, properties, raw_managers):
    assert isinstance(raw_managers, dict)
    all_combs = get_all_dict_combinations(properties)
    all_features = []
    feature_representation = {}
    for comb in all_combs:
        assert 'raw_data_manager' in comb.keys()
        assert comb['raw_data_manager'] in raw_managers.keys()
        representation = feature_name + "_" + '_'.join([str(i) for i in comb.values()])

        comb['raw_data_manager'] = raw_managers[comb['raw_data_manager']]
        feature_instance = create_feature(feature_name, comb)
        all_features.append(feature_instance)

        feature_representation[representation] = feature_instance

    return all_features, feature_representation


def create_feature_import_string(all_dicts):
    pass


def create_feature_list_string(all_dicts):
    pass


def create_feature_init_string(all_dicts):
    pass


def stringigy_properties(properties):
    pass


def trim_combined_properties(r):
    pass


def generate_alpha_file(alpha_name, features):
    assert isinstance(features, dict)
    assert isinstance(alpha_name, str)
    f = open('alpha_template', 'r')
    dd = {'featureImport': '', 'featureList': '', 'featureInit': '', 'alphaName': alpha_name}
    template = f.read()
    feat_list = [i.lower() for i in features.keys()]
    feature_list = ', '.join(feat_list)
    print(feature_list)

    res = template.format(**dd)


def generate_csv_files(data_managers_path):
    all_ff = parse_yaml(data_managers_path)[1]
    managers = Get_period_only_managers(data_managers_path)

    for time_frame, manager in managers.items():
        pp = manager.get_backfill_df()
        assert isinstance(pp, pd.DataFrame)
        for feature_group in all_ff:
            assert isinstance(feature_group, dict)
            for feature_representation, feature_instance in feature_group.items():
                assert isinstance(feature_representation, str)
                assert isinstance(feature_instance, EmptyFeature)
                if time_frame in feature_representation:
                    pp[feature_representation] = feature_instance.get_TS()

        path = 'data_test/features/' + time_frame + '.csv'

        pp.to_csv(path, index_label='time')


# returns yaml data and template strings
def parse_yaml(data_managers_path):

    with open("alpha.yaml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            yy = {}

            all_features = []
            # template_strings = []
            for alpha_name, alpha_properties in data.items():
                features = alpha_properties['Features']
                all_ff_dict = {}
                # template_string = {'featureImport': '', 'featureList': '', 'featureInit': '', 'alphaName': alpha_name}
                for feature_name, feature_properties in features.items():
                    all_ff_dict[feature_name] = get_all_feature_combinations(feature_name, feature_properties, Get_period_only_managers(data_managers_path))[0]
                    all_features.append(get_all_feature_combinations(feature_name, feature_properties, Get_period_only_managers(data_managers_path))[1])
                yy[alpha_name] = all_ff_dict

            return yy, all_features

        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    generate_csv_files('data/store/binanceBTCUSDT.p')
