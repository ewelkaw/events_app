from app.models import WebSource

from . import main


def link_to_source(source, classes=""):
    return f'<a href="/service/{source.source_name}" class={classes}>{source.source_name}</a>'


main.add_app_template_global(link_to_source)


@main.add_app_template_global
def link_to_date(date):
    return f'<a href="/date/{date}">{date}</a>'


@main.add_app_template_global
def list_services():
    return "".join(
        list(
            map(
                lambda x: link_to_source(x, classes="navbar-brand"),
                WebSource.query.all(),
            )
        )
    )
