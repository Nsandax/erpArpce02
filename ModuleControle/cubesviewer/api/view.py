from django.db.models import Q

from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from ModuleControle.models import CubesView
from django.views.decorators.csrf import csrf_exempt


class CubesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CubesView
        #fields = ('url', 'username', 'email', 'groups')


class ViewSaveView(APIView):

    #model = Match
    #serializer_class = MatchSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        #tview = None

        if (int(request.data["id"]) > 0):
            tview = CubesView.objects.get(pk = request.data["id"])
            if (tview.owner_id != request.user.id):
                raise Exception("Cannot save View belonging to other users.")
        else:
            tview = CubesView()

        # Update or delete as necessary
        if (request.data["data"] == u""):
            tview.delete()
        else:
            tview.name = request.data["name"]
            tview.data = request.data["data"]
            tview.owner = request.user
            if (request.data["shared"] == True):
                tview.shared = True
            else:
                tview.shared = False

            tview.save()

        serializer = CubesViewSerializer(tview, many=False, context={'request': request})
        return Response(serializer.data)


class ViewListView(APIView):

    #model = Match
    #serializer_class = MatchSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        views = CubesView.objects.filter(Q(owner=request.user) | Q(shared=True))
        serializer = CubesViewSerializer(views, many=True, context={'request': request})
        return Response(serializer.data)


