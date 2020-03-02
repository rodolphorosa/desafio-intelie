class SchemaFacts:
    """
    This class provides the tools to visualize and manipulate facts and schema.
    The constructor input comprises two lists of tuples: schema and facts.
    """
    def __init__(self, schema, facts):
        self.__schema = schema
        self.__facts = facts

    @staticmethod
    def __retrieve_facts_by_entity(facts, entity):
        """
        Given a list of facts and an entity, returns the facts that related to this entity.
        :param facts: List of facts
        :param entity: Entity's name
        :return: Facts of the entity
        """
        return list(filter(lambda f: f[0] == entity, facts))

    @staticmethod
    def __retrieve_facts_by_attribute(facts, attribute):
        """
        Given a list of facts and an attribute, returns all the facts related to this attribute.
        :param facts: List of facts
        :param attribute: Attribute's name
        :return: Facts of the attribute
        """
        return list(filter(lambda f: f[1] == attribute, facts))

    @staticmethod
    def __retrieve_deleted_facts(facts):
        """
        Given a list of facts, returns the ones whose field 'added' has value False
        :param facts: List of facts
        :return: Facts with added False
        """
        return list(filter(lambda f: f[3] is False, facts))

    @staticmethod
    def __retrieve_non_deleted_facts(facts):
        """
        Given a list of facts, returns the ones whose field 'added' has value True
        :param facts: List of facts
        :return: Facts with added True
        """
        return list(filter(lambda f: f[3] is True, facts))

    @staticmethod
    def __retrieve_attribute_by_name(schema, attribute):
        """
        Given a schema and an attribute, returns the tuple corresponding to this attribute
        :param schema: List of attributes
        :param attribute: Attribute's name
        :return: Tuple of attribute
        """
        return list(filter(lambda a: a[0] == attribute, schema))[0]

    @staticmethod
    def __drop_facts_by_attribute(facts, attribute):
        """
        Given a list of facts and an attribute, deletes the facts related to this attribute
        :param facts: List of facts
        :param attribute: Attribute's name
        :return: None
        """
        for fact in facts:
            if fact[1] == attribute:
                facts[facts.index(fact)] = (fact[0], fact[1], fact[2], False)

    @staticmethod
    def __drop_facts_by_entity(facts, entity):
        """
        Given a list of facts and an entity, deletes the facts related to this entity
        :param facts: List of facts
        :param entity: Entity's name
        :return: None
        """
        for fact in facts:
            if fact[0] == entity:
                facts[facts.index(fact)] = (fact[0], fact[1], fact[2], False)

    def get_schema(self):
        """
        Returns the list of all attributes (schema).
        :return: Schema
        """
        return self.__schema

    def get_facts(self):
        """
        Returns the list of all facts (current or not).
        :return: All facts.
        """
        return self.__facts

    def get_attribute(self, attribute):
        """
        Returns the tuple corresponding to an attribute.
        :param attribute: Attribute's name
        :return: Attribute's corresponding tuple.
        """
        return self.__retrieve_attribute_by_name(self.__schema, attribute)

    def get_current_facts(self):
        """
        This method is responsible for retrieving all current facts.
        :return: list of all current fats.
        """
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

    def insert_attribute(self, attribute, cardinality):
        """
        Verifies if attribute already exists in the schema, and then inserts it to it if it does not.
        :param attribute: Attribute to be inserted.
        :param cardinality: Attribute's cardinality ('one' or 'many')
        :return: None
        """
        if attribute in [s[0] for s in self.__schema]:
            raise Exception("Attribute already exists")
        else:
            self.__schema.append((attribute, 'cardinality', cardinality))

    def insert_fact(self, entity, attribute, value):
        """
        First verifies if attribute exists, and then inserts the fact into the fact list.
        :param entity: Entity of the fact.
        :param attribute: Attribute of the entity.
        :param value: Value of the attribute.
        :return: None
        """
        if attribute not in [s[0] for s in self.__schema]:
            raise Exception("Attribute \'{0}\' not in schema".format(attribute))
        else:
            self.__facts.append((entity, attribute, value, True))

    def update_attribute(self, attribute, cardinality):
        """
        Verifies if attribute exists, and the update its cardinality.
        :param attribute: Attribute's name.
        :param cardinality: New cardinality.
        :return: None
        """
        if attribute not in [s[0] for s in self.__schema]:
            raise Exception("Attribute not found")
        else:
            for attr in range(len(self.__schema)):
                if self.__schema[attr][0] == attribute:
                    self.__schema[attr] = (attribute, 'cardinality', cardinality)

    def delete_attribute(self, attribute):
        """
        Deletes an attribute of schema, if it exists.
        :param attribute: Attribute's name.
        :return: None
        """
        attr = [attr for attr in self.__schema if attr[0] == attribute]
        if len(attr) == 0:
            raise Exception("Attribute \'{0}\' not in schema".format(attribute))
        else:
            self.__schema.remove(attr[0])
            self.__drop_facts_by_attribute(self.__facts, attribute)

    def delete_fact(self, entity, attribute, value):
        """
        Deletes a fact of the fact list.
        :param entity: Entity of the fact.
        :param attribute: Attribute of the fact.
        :param value: Value of the attribute.
        :return: None
        """
        self.__facts.append((entity, attribute, value, False))


if __name__ == '__main__':
    facts = [
        ('entity/1', 'name', 'gabriel', True),
        ('entity/1', 'address', 'av rio branco, 109', True),
        ('entity/2', 'address', 'rua alice, 10', True),
        ('entity/2', 'name', 'joão', True),
        ('entity/2', 'address', 'rua bob, 88', True),
        ('entity/2', 'phone', '234-5678', True),
        ('entity/2', 'phone', '91234-5555', True),
        ('entity/2', 'phone', '234-5678', False),
        ('entity/1', 'phone', '98888-1111', True),
        ('entity/1', 'phone', '56789-1010', True),
        ('entity/2', 'address', 'rua bob, 88', False)
    ]

    schema = [
        ('name', 'cardinality', 'one'),
        ('address', 'cardinality', 'one'),
        ('phone', 'cardinality', 'many')
    ]

    sf = SchemaFacts(schema, facts)

    for fact in sf.get_current_facts():
        print(fact)
