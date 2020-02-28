from lxml import etree as et


class DataHandler:
    def __init__(self, xml_file_path):
        self.__xml_file_path = xml_file_path

    def restore_data(self):
        facts = []
        schema = []

        parser = et.XMLParser(remove_blank_text=True)
        xml = et.parse(self.__xml_file_path, parser)
        data = xml.getroot()

        for attribute in data.find("schema").iter("attribute"):
            name = attribute.get("name")
            cardinality = attribute.find("cardinality").text

            schema.append((name, "cardinality", cardinality))

        for fact in data.find("facts").iter("fact"):
            is_current = fact.get("current")
            entity = fact.find("entity").text
            attribute = fact.find("attribute").text
            value = fact.find("value").text
            added = True if is_current == "yes" else False

            facts.append((entity, attribute, value, added))
        return schema, facts

    def save_data(self, schema, facts):
        data = et.Element('data')
        this_schema = et.SubElement(data, "schema")
        for attr in schema:
            attribute = et.SubElement(this_schema, "attribute")
            cardinality = et.SubElement(attribute, "cardinality")
            attribute.set("name", attr[0])
            cardinality.text = attr[2]

        this_facts = et.SubElement(data, "facts")
        for f in facts:
            fact = et.SubElement(this_facts, "fact")
            entity = et.SubElement(fact, "entity")
            attribute = et.SubElement(fact, "attribute")
            value = et.SubElement(fact, "value")
            fact.set("current", 'yes' if f[3] else 'no')
            entity.text = f[0]
            attribute.text = f[1]
            value.text = f[2]

        base = et.tostring(data, encoding="unicode", pretty_print=True)
        with open(self.__xml_file_path, "w", encoding="utf-8") as file:
            file.write(base)


class HistoryHandler:
    def __init__(self, xml_file_path):
        self.__xml_file_path = xml_file_path

    def register_modification(self, modification):
        parser = et.XMLParser(remove_blank_text=True)
        modifications = None
        try:
            xml = et.parse(self.__xml_file_path, parser)
            modifications = xml.getroot()
        except Exception as e:
            modifications = et.Element('modifications')
        finally:
            HistoryHandler.__create_modification_tree(
                modifications,
                modification["action"],
                modification["entity"],
                modification["attribute"],
                modification["value"],
                modification["datetime"]
            )
            base = et.tostring(modifications, encoding="unicode", pretty_print=True)
            with open(self.__xml_file_path, "w", encoding="utf-8") as file:
                file.write(base)

    def retrieve_entity_modification_history(self, entity):
        parser = et.XMLParser(remove_blank_text=True)
        try:
            xml = et.parse(self.__xml_file_path, parser)
            modifications = xml.getroot()

            history = []

            for modification in modifications.iter("modification"):
                if modification.find("entity").text == entity:
                    attribute = modification.find("attribute").text
                    value = modification.find("value").text
                    datetime = modification.find("date_time").text
                    action = modification.get("action")

                    history.append({
                        "datetime": datetime,
                        "entity": entity,
                        "attribute": attribute,
                        "value": value,
                        "action": action
                    })
            return history
        except Exception as e:
            return None

    @staticmethod
    def __create_modification_tree(root, action, entity, attribute, value, date_time):
        modification = et.SubElement(root, "modification")
        child_entity = et.SubElement(modification, "entity")
        child_attribute = et.SubElement(modification, "attribute")
        child_value = et.SubElement(modification, "value")
        child_date_time = et.SubElement(modification, "date_time")

        modification.set("action", action)
        child_entity.text = entity
        child_attribute.text = attribute
        child_value.text = value
        child_date_time.text = date_time

        return modification


class UserHandler:
    def __init__(self, xml_file_path):
        self.__xml_file_path = xml_file_path

    def retrieve_user(self, username, password):
        parser = et.XMLParser(remove_blank_text=True)
        xml = et.parse(self.__xml_file_path, parser)
        users = xml.getroot()

        for user in users.iter("user"):
            if user.find("username").text == username and user.find("password").text == password:
                return {"username": user.find("username").text, "role": user.get("role")}
        return None


if __name__ == '__main__':
    pass
