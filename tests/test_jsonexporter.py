import filecmp

from tempfile import NamedTemporaryFile

from nose.tools import eq_

from anytree import AnyNode
from anytree.exporter import JsonExporter


def test_json_exporter():
    """Json Exporter."""
    root = AnyNode(id="root")
    s0 = AnyNode(id="sub0", parent=root)
    AnyNode(id="sub0B", parent=s0)
    AnyNode(id="sub0A", parent=s0)
    s1 = AnyNode(id="sub1", parent=root)
    AnyNode(id="sub1A", parent=s1)
    AnyNode(id="sub1B", parent=s1)
    s1c = AnyNode(id="sub1C", parent=s1)
    AnyNode(id="sub1Ca", parent=s1c)

    lines = [
        '{',
        '  "children": [',
        '    {',
        '      "children": [',
        '        {',
        '          "id": "sub0B"',
        '        },',
        '        {',
        '          "id": "sub0A"',
        '        }',
        '      ],',
        '      "id": "sub0"',
        '    },',
        '    {',
        '      "children": [',
        '        {',
        '          "id": "sub1A"',
        '        },',
        '        {',
        '          "id": "sub1B"',
        '        },',
        '        {',
        '          "children": [',
        '            {',
        '              "id": "sub1Ca"',
        '            }',
        '          ],',
        '          "id": "sub1C"',
        '        }',
        '      ],',
        '      "id": "sub1"',
        '    }',
        '  ],',
        '  "id": "root"',
        '}'
    ]

    exporter = JsonExporter(indent=2, sort_keys=True)
    exported = exporter.export(root).split("\n")
    exported = [e.rstrip() for e in exported]  # just a fix for a strange py2x behavior.
    eq_(exported, lines)
    with NamedTemporaryFile(mode="w+") as ref:
        with NamedTemporaryFile(mode="w+") as gen:
            ref.write("\n".join(lines))
            exporter.write(root, gen)
            assert filecmp.cmp(ref.name, gen.name)
