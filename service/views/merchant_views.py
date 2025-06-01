from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.dateparse import parse_datetime
from service.models import Campaign


class SendNotificationRequestSerializer(serializers.Serializer):
    campaign_id = serializers.IntegerField()
    idempotency_key = serializers.CharField()


class ScheduleNotificationRequestSerializer(serializers.Serializer):
    campaign_id = serializers.IntegerField()
    scheduled_time = serializers.DateTimeField()


@swagger_auto_schema(
    method="post",
    request_body=SendNotificationRequestSerializer,
    responses={
        202: openapi.Response("Accepted"),
        400: "Bad Request",
        404: "Not Found",
        200: "Already Processed",
    },
)
@api_view(["POST"])
def send_notification(request):
    idempotency_key = request.data.get("idempotency_key")
    campaign_id = request.data.get("campaign_id")

    if not campaign_id or not idempotency_key:
        return Response(
            {"error": "campaign_id and idempotency_key required"}, status=400
        )

    existing = Campaign.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        return Response(
            {"message": "Already processed", "campaign_id": existing.id}, status=200
        )

    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return Response({"error": "Campaign not found"}, status=404)

    if campaign.recipients.count() == 0 or campaign.templates.count() == 0:
        return Response({"error": "Recipients and templates required"}, status=400)

    campaign.idempotency_key = idempotency_key
    campaign.status = "processing"
    campaign.save()

    campaign.trigger_immediate()

    return Response(
        {"message": "Campaign sent", "campaign_id": campaign.id}, status=202
    )


@swagger_auto_schema(
    method="post",
    request_body=ScheduleNotificationRequestSerializer,
    responses={202: "Scheduled", 400: "Bad Request", 404: "Not Found"},
)
@api_view(["POST"])
def schedule_notification(request):
    campaign_id = request.data.get("campaign_id")
    scheduled_time = request.data.get("scheduled_time")

    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return Response({"error": "Campaign not found"}, status=404)

    if not scheduled_time:
        return Response({"error": "scheduled_time is required"}, status=400)

    campaign.scheduled_time = parse_datetime(scheduled_time)
    campaign.schedule_task()
    campaign.status = "scheduled"
    campaign.save()

    return Response(
        {"message": "Campaign scheduled", "campaign_id": campaign.id}, status=202
    )


@swagger_auto_schema(
    method="delete",
    manual_parameters=[
        openapi.Parameter(
            "campaign_id",
            openapi.IN_PATH,
            description="Campaign ID",
            type=openapi.TYPE_INTEGER,
        )
    ],
    responses={200: "Cancelled", 400: "Invalid Status", 404: "Not Found"},
)
@api_view(["DELETE"])
def cancel_scheduled_notification(request, campaign_id):
    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return Response({"error": "Campaign not found"}, status=404)

    if campaign.status != "scheduled":
        return Response(
            {"error": "Only scheduled campaigns can be cancelled"}, status=400
        )

    campaign.cancel_scheduled_task()
    campaign.status = "cancelled"
    campaign.save()

    return Response(
        {"message": "Campaign cancelled", "campaign_id": campaign.id}, status=200
    )


@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "campaign_id",
            openapi.IN_PATH,
            description="Campaign ID",
            type=openapi.TYPE_INTEGER,
        )
    ],
    responses={200: openapi.Response("Campaign status")},
)
@api_view(["GET"])
def get_campaign_status(request, campaign_id):
    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return Response({"error": "Campaign not found"}, status=404)

    return Response(
        {
            "campaign_id": campaign.id,
            "status": campaign.status,
            "scheduled_time": campaign.scheduled_time,
            "created_at": campaign.created_at,
        }
    )
