from .models import Login

def get_user_counts_context():
    camp_count = Login.objects.filter(usertype='camp').count()
    police_station_count = Login.objects.filter(usertype='police_station').count()
    public_user_count = Login.objects.filter(usertype='public_user').count()
    volunteer_count = Login.objects.filter(usertype='volunteer').count()

    return {
        'camp_count': camp_count,
        'police_station_count': police_station_count,
        'public_user_count': public_user_count,
        'volunteer_count': volunteer_count,
    }