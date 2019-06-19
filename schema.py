import graphene
import json
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    last_login = graphene.DateTime()


class Query(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(self, info):
        return [
            User(username='VK', last_login=datetime.now()),
            User(username='Callum', last_login=datetime.now())
        ]


schema = graphene.Schema(query=Query)

result = schema.execute(
    '''
    {
        users {
            username
            lastLogin
        }
    }
    '''
)

items = dict(result.data.items())

print(json.dumps(items, indent=4))
