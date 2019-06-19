import graphene
import json
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    last_login = graphene.DateTime(required=False)


class Query(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(self, info):
        return [
            User(username='VK', last_login=datetime.now()),
            User(username='Callum', last_login=datetime.now())
        ]


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()

    user = graphene.Field(User)

    def mutate(self, info, username):
        if info.context.get('is_organisation_owner'):
            username = username.upper()

        user = User(username=username)
        return CreateUser(user=user)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)

# return list of users with their username and las login
# result = schema.execute(
#     '''
#     {
#         users {
#             username
#             lastLogin
#         }
#     }
#     '''
# )

# return list of users with their username and las login
result = schema.execute(
    '''
    mutation createUser($username: String) {
        createUser(username: $username) {
            user {
                username 
            }
        }
    }
    ''',
    variable_values={'username': 'Ben'},
    context={'is_organisation_owner': True}
)


items = dict(result.data.items())

print(json.dumps(items, indent=4))
