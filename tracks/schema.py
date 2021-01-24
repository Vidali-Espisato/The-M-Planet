import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from .models import Track, Like
from users.schema import UserType
from django.db.models import Q

class TrackType(DjangoObjectType):
    class Meta:
        model = Track

class LikeType(DjangoObjectType):
    class Meta:
        model = Like

class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType, search=graphene.String())
    likes = graphene.List(LikeType)

    def resolve_tracks(self, info, search=None):
        if search:
            # filters = (
            #     Q(title__icontains=search) |
            #     Q(description__icontains=search) |
            #     Q(url__icontains=search) |
            #     Q(posted_by__username__icontains=search) 
            # )
            filters = eval("|".join([f"Q({f}__icontains=search)" for f in ["title", "description", "url", "posted_by__username"]]))
            return Track.objects.filter(filters)
        return Track.objects.all()

    def resolve_likes(self, info):
        return Like.objects.all()    


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Login required!")
        track = Track(title=title, description=description, url=url, posted_by=user)
        track.save()
        return CreateTrack(track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, track_id, title, description, url):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        if track.posted_by != user:
            raise GraphQLError("Updation not permitted")
        track.title = title
        track.description = description
        track.url = url
        return UpdateTrack(track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int()
    title = graphene.String()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        track = Track.objects.get(id=track_id)
        title = track.title
        if track.posted_by != user:
            return GraphQLError("Deletion not permitted")
        track.delete()
        return DeleteTrack(track_id=track_id, title=title)


class CreateLike(graphene.Mutation):
    track = graphene.Field(TrackType)
    user = graphene.Field(UserType)

    class Arguments:
        track_id = graphene.Int()

    def mutate(self, info, track_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Logged in user required")
        track = Track.objects.get(id=track_id)
        if not track:
            raise GraphQLError("Track not found")
        Like.objects.create(user=user, track=track)
        return CreateLike(user=user, track=track)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()