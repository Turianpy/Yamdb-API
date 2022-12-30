from rest_framework import mixins, viewsets, status
from rest_framework.response import Response


class CreateListDelVS(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        paginated_response = self.list(request, *args, **kwargs)
        return Response(
            paginated_response.data,
            status=status.HTTP_201_CREATED
        )
