from celery import shared_task


@shared_task(name="Process Campaign")
def process_campaign(campaign_id):
    from service.models import Campaign

    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return f"Campaign {campaign_id} not found"

    # Update status
    campaign.status = "processing"
    campaign.save()

    # Simulate sending logic here
    # e.g., notify_via_email(template, recipient)

    campaign.status = "completed"
    campaign.save()

    return f"Processed Campaign {campaign_id}"
