#!/usr/bin/env python

from google.cloud import datastore

class DSHelper():
    """Utility class to support work with Google DataStore"""
    def __enter__(self):
        return self

    def __init__(self, config):
        try:
            # self.logging = SDHelper(config)

            self.project_id = config['project-id']
            # self.kind = config['kind'] if 'kind' in config else False
            self.client = datastore.Client(self.project_id)
        except Exception as e:
            msg = 'DSHelper.__init__ -> Details: ' + str(e)
            # self.logging.logEvent(msg, severity='ERROR', jobstatus='START', logContext=msg)
            raise RuntimeError(msg)
    
    def insert(self, new_entity, kind=False):
        """
        Insert a new entity into DataStore.

        If the "Kind" does not already exist, when you create your first entity
        it will automatically be created.

        INPUTS:
        new_entity = {'property1': 'values',
                    'property2': 'values'
                    }
        kind = 'DataStore Kind' # Optional if a kind is specified in the config

        OUTPUTS:
        entity_id (if return_id is set to True)
        """
        # TODO: do you want to combine the insert and update functions?

        try:
            kind = kind or self.kind
            key = self.client.key(kind)
            entity = datastore.Entity(key=key)
            entity.update(new_entity)
            self.client.put(entity)

            return entity.key.id

        except Exception as e:
            msg = 'DSHelper.upsert -> Details: ' + str(e)
            self.logging.logEvent(msg, severity='ERROR', jobstatus='INPROGRESS', logContext=msg)
            raise RuntimeError(msg)
    
    def update(self, entity_id, new_entity, kind=False):
        """
        Update an entity by its id.

        INPUTS:
        entity_id = 'DataStore entity id'
        new_entity = {'property': 'value'}
        kind = 'DataStore kind' # Optional if a kind is specified in the config

        OUTPUTS:
        query object
        """
        try:
            kind = kind or self.kind
            key = self.client.key(kind, entity_id)

            entity = datastore.Entity(key=key)

            entity.update(new_entity)

            self.client.put(entity)
        except Exception as e:
            msg = 'DSHelper.update -> Details: ' + str(e)
            # self.logging.logEvent(msg, severity='ERROR', jobstatus='INPROGRESS', logContext=msg)
            raise RuntimeError(msg)

    def batchUpsert(self, entities):
        """
        Upsert -> insert or update.

        INPUTS:
        entities = [{'kind': 'DataStore Kind',
                    'entity': {'property1': 'value1',
                                'property2': 'value2'
                                }
                    },
                    {'kind': 'DataStore Kind',
                    'entity': {'property1': 'value1',
                                'property2': 'value2'
                                }
                    }
                ]

        OUTPUTS:
        No output
        """
        try:
            # kind = entity['kind'] if 'kind' in entity else self.kind
            inserts = []
            for n, entity in enumerate(entities):
                if 'entity_id' in entity:
                    inserts.append(datastore.Entity(self.client.key(entity['kind'], entity['entity_id'])))
                else:
                    inserts.append(datastore.Entity(self.client.key(entity['kind'])))

                inserts[n].update(entity['entity'])

            self.client.put_multi(inserts)
        except Exception as e:
            msg = 'DSHelper.batchUpsert -> Details: ' + str(e)
            # self.logging.logEvent(msg, severity='ERROR', jobstatus='INPROGRESS', logContext=msg)
            raise RuntimeError(msg)

    def getAllIds(self, kind=False):
        """
        Get all entity ids for a specific kind

        INPUTS:
        kind = 'DataStore kind' # Optional if a kind is specified in the config

        OUTPUTS:
        entity # a DataStore entity
        """
        try:
            kind = kind or self.kind
            query = self.client.query(kind=kind)
            query.keys_only()
            return list(map(lambda x: x.key.id, query.fetch()))
        except Exception as e:
            msg = 'DSHelper.getAllIds -> Details: ' + str(e)
            # self.logging.logEvent(msg, severity='ERROR', jobstatus='INPROGRESS', logContext=msg)
            raise RuntimeError(msg)

    def getEntityById(self, entity_id, kind=False):
        """
        Get an entity by its id.

        INPUTS:
        entity_id = 'DataStore entity id'
        kind = 'DataStore kind' # Optional if a kind is specified in the config

        OUTPUTS:
        entity # dictionary of datastore entity
        """
        try:
            kind = kind or self.kind
            key = self.client.key(kind, entity_id)
            obj = self.client.get(key)
            if obj is not None:
                entity = dict(obj)
                entity['key'] = obj.key.id
                return entity
            else:
                return None
        except Exception as e:
            msg = 'DSHelper.getEntityById -> Details: ' + str(e)
            # self.logging.logEvent(msg, severity='ERROR', jobstatus='INPROGRESS', logContext=msg)
            raise RuntimeError(msg)

    def query(self, filters=[], kind=False ):
        """
        Queries everything in a DataStore kind.

        INPUTS:
        filters = list of 3-ples (field, relation, value) eg ('field','=',7)
        kind = 'DataStore kind' # Optional if a kind is specified in the config

        OUTPUTS:
        list containing DataStore entities
        Reference: https://cloud.google.com/datastore/docs/concepts/queries
        """
        try:
            kind = kind or self.kind
            query = self.client.query(kind=kind)
            if len(filters) > 0:
                for field, reln, val in filters:
                    query.add_filter(field, reln, val)

            return list(query.fetch()) # this is an iterable

        except Exception as e:
            msg = 'DSHelper.query -> Details: ' + str(e)
            # self.logging.logEvent(msg, severity='ERROR', jobstatus='INPROGRESS', logContext=msg)
            raise RuntimeError(msg)
    
    def batchRead(self, entities):
        """
        Get a list of entities by id.

        INPUTS:
        entities = [{'kind': 'DataStore Kind',
                     'entity_id': 123
                    },
                    {'kind': 'DataStore Kind',
                     'entity_id': 133
                    }
                   ]

        OUTPUTS:
        List of entities
        """
        try:
            gets = []
            for n, entity in enumerate(entities):
                gets.append(self.client.key(entity['kind'], entity['entity_id']))

            return self.client.get_multi(gets)
        except Exception as e:
            msg = 'DSHelper.batchRead -> Details: ' + str(e)
            # self.logging.logEvent(msg, severity='ERROR', jobstatus='INPROGRESS', logContext=msg)
            raise RuntimeError(msg)


    def __exit__(self, type, value, traceback):
        pass
