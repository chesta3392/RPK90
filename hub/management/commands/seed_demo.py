from django.core.management.base import BaseCommand
from hub.models import Game, Notice, Result
from datetime import date
class Command(BaseCommand):
    help = "Add sample games, notices and results"
    def handle(self, *args, **kwargs):
        names = ["Morning Star","Silver City","London Bazar","Delhi Bazaar","Dev Darshan","Shri Ganesh","HR // 20","Faridabad","India Club","Demo"]
        for i, name in enumerate(names): Game.objects.get_or_create(name=name, defaults={"sort_order":i})
        Notice.objects.get_or_create(title="Welcome to Demo Play Hub", defaults={"body":"This prototype uses simulated points and sample data only."})
        for name in names[:5]: Result.objects.get_or_create(game_name=name, result_date=date.today(), defaults={"result_value":"07"})
        self.stdout.write(self.style.SUCCESS("Demo data created."))
