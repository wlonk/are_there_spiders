from django.contrib import admin
from .models import Artwork, Review


class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('flagged_by', )
    list_display = ('__unicode__', 'flagged_count', 'marked_as_spam')


admin.site.register(Artwork)
admin.site.register(Review, ReviewAdmin)
