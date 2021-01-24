import graphene
import graphql_jwt
import tracks.schema as tschema
import users.schema as uschema

class Query(uschema.Query, tschema.Query, graphene.ObjectType):
    pass


class Mutation(uschema.Mutation, tschema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)