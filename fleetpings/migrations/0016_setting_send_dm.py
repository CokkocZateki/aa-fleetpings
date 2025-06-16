from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fleetpings", "0015_alter_discordpingtarget_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="setting",
            name="send_direct_messages",
            field=models.BooleanField(
                default=False,
                db_index=True,
                help_text="Send fleet pings as Discord direct messages instead of posting to a webhook.",
                verbose_name="Send direct messages",
            ),
        ),
    ]
