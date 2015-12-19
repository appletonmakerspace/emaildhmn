'''
Currently running on a host with Python 2.6.1, hence no collections.Counter()'s
'''
import feedparser
from string import Template


class RecentWikiEdits:

    def fetch(self):
        d = feedparser.parse('https://server.appletonmakerspace.org/wiki/feed.php?type=atom1&mode=recent&minor=1&view=both')

        editor_counts = {}

        for foo in d.entries:
            if foo.author in editor_counts:
                editor_counts[foo.author] += 1
            else:
                editor_counts[foo.author] = 1

        most_recent_edit_string = '\n        - ' + d.entries[0].author + ' edited "' + d.entries[0].title + '" at ' + d.entries[0].published

        most_prolific_editors = sorted(editor_counts, key=editor_counts.get, reverse=True)[:3]

        most_prolific_editors_string = ''

        for editor in most_prolific_editors:
            most_prolific_editors_string += '\n        - ' + editor + ': ' + str(editor_counts[editor]) + ' edits.'

        output_template = Template('''    Most recent edit:
        $edit

    Most recently prolific editors:
        $editors

    Surely this cannot stand! You can best those paltry edit numbers to become *THIS* weeks most prolific wiki editor!
    https://server.appletonmakerspace.org/wiki''')

        return output_template.substitute(
            edit=most_recent_edit_string,
            editors=most_prolific_editors_string
        )
