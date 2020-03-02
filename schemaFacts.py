from pprint import pprint
from xmlHandler import DataHandler


class SchemaFacts:
    def __init__(self, schema, facts):
        self.__schema = schema
        self.__facts = facts

    @staticmethod
    def __retrieve_facts_by_entity(facts, entity):
        return list(filter(lambda f: f[0] == entity, facts))

    @staticmethod
    def __retrieve_facts_by_attribute(facts, attribute):
        return list(filter(lambda f: f[1] == attribute, facts))

    @staticmethod
    def __retrieve_deleted_facts(facts):
        return list(filter(lambda f: f[3] is False, facts))

    @staticmethod
    def __retrieve_non_deleted_facts(facts):
        return list(filter(lambda f: f[3] is True, facts))

    @staticmethod
    def __retrieve_attribute_by_name(schema, attribute_name):
        return list(filter(lambda a: a[0] == attribute_name, schema))[0]

    @staticmethod
    def __drop_facts_by_attribute(facts, attribute):
        for fact in facts:
            if fact[1] == attribute:
                facts[facts.index(fact)] = (fact[0], fact[1], fact[2], False)

    @staticmethod
    def __drop_facts_by_entity(facts, entity):
        for fact in facts:
            if fact[0] == entity:
                facts[facts.index(fact)] = (fact[0], fact[1], fact[2], False)

    def get_schema(self):
        return self.__schema

    def get_facts(self):
        return self.__facts

    def get_attribute(self, attribute):
        return self.__retrieve_attribute_by_name(self.__schema, attribute)

    def get_current_facts(self):
        deleted_facts = self.__retrieve_deleted_facts(self.__facts)
        non_deleted_facts = self.__retrieve_non_deleted_facts(self.__facts)

        current_facts = []
        for attribute in self.__schema:
            facts_by_attribute = self.__retrieve_facts_by_attribute(non_deleted_facts, attribute[0])
            if attribute[2] == 'one':
                for entity in set([f[0] for f in facts_by_attribute]):
                    current_facts.append(self.__retrieve_facts_by_entity(facts_by_attribute, entity)[-1])
            else:
                current_facts += facts_by_attribute

        for df in deleted_facts:
            for cf in current_facts:
                if cf[0:3] == df[0:3]:
                    current_facts.remove(cf)

        return current_facts

    def insert_attribute(self, attribute_name, attribute_value):
        if attribute_name in [s[0] for s in self.__schema]:
            raise Exception("Attribute already exists")
        else:
            self.__schema.append((attribute_name, 'cardinality', attribute_value))

    def insert_fact(self, entity, attribute, value):
        if attribute not in [s[0] for s in self.__schema]:
            raise Exception("Attribute \'{0}\' not in schema".format(attribute))
        else:
            self.__facts.append((entity, attribute, value, True))

    def update_attribute(self, attribute_name, attribute_value):
        if attribute_name not in [s[0] for s in self.__schema]:
            raise Exception("Attribute not found")
        else:
            for attr in range(len(self.__schema)):
                if self.__schema[attr][0] == attribute_name:
                    self.__schema[attr] = (attribute_name, 'cardinality', attribute_value)

    def delete_attribute(self, attribute):
        attr = [attr for attr in self.__schema if attr[0] == attribute]
        if len(attr) == 0:
            raise Exception("Attribute \'{0}\' not in schema".format(attribute))
        else:
            self.__schema.remove(attr[0])
            self.__drop_facts_by_attribute(self.__facts, attribute)

    def delete_fact(self, entity, attribute, value):
        self.__facts.append((entity, attribute, value, False))


if __name__ == '__main__':
    pass
