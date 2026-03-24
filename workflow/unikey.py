import sys

HELP = """unikey preprocessor

KEYS:
  hd, /head       ### text <!-- HEAD -->
  ne, /name       #### text <!-- NAME -->
  ce, /code       ```CODE ... ```
  ct, /comment    > text
  lt, /list       ### text <!-- LIST -->  (enters list mode)

LIST MODE (after lt, /list):
  -               - item
  --                  - subitem
  any other key   exits list mode

EXAMPLE INPUT:
  hd Title
  lt Sections
  - First
  -- Nested
  ne Item Name
  ct Some comment
  ce code

EXAMPLE OUTPUT:
  ### Title <!-- HEAD -->
  ### Sections <!-- LIST -->
  - First
      - Nested
  #### Item Name <!-- NAME -->
  > Some comment
  ```CODE
  code
  ```
"""

KEYS_LIST = ['-', '--']
KEYS = ['hd', '/head', 'ce', '/code', 'ne', '/name', 'ct', '/comment', 'lt', '/list']

CANON = {
    'hd': 'hd', '/head': 'hd',
    'ne': 'ne', '/name': 'ne',
    'ce': 'ce', '/code': 'ce',
    'ct': 'ct', '/comment': 'ct',
    'lt': 'lt', '/list': 'lt',
}

def tokenize_input(input_str):
    tokens, word = [], ""
    for char in input_str:
        if char.isspace():
            if word:
                tokens.append(word)
                word = ""
            tokens.append(char)
        else:
            word += char
    if word:
        tokens.append(word)
    return tokens

def clean_data(data):
    if data and data[0].startswith(' '):
        data = data[1:]
    if data and (data[-1].endswith(' ') or data[-1].endswith('\n')):
        data = data[:-1]
    return data

def join_data(data):
    return ' '.join(''.join(data).split())

def format_output(key, data, ctx, fmt):
    key = CANON.get(key, key)
    data = clean_data(data)
    ctx = ctx.copy()

    if all(not s.strip() for s in data):
        if key == 'lt':
            ctx['MODE_LIST_lt'] = True
        else:
            print(f"[DEBUG] Key '{key}' without data")
        return None, ctx

    joined = join_data(data)

    if fmt == 'md':
        if ctx['MODE_LIST_lt']:
            if key == '-':
                return f"- {joined}", ctx
            if key == '--':
                return f"    - {joined}", ctx
            return None, ctx

        formats = {
            'hd': f"\n### {joined} <!-- HEAD -->",
            'ce': f"\n```CODE\n{''.join(data)}\n```",
            'ne': f"\n#### {joined} <!-- NAME -->",
            'ct': f"\n> {joined}",
        }
        if key == 'lt':
            ctx['MODE_LIST_lt'] = True
            return f"\n### {joined} <!-- LIST -->", ctx

        return formats.get(key), ctx

    return None, ctx

def process_tokens(tokens, fmt):
    output, context = [], {'MODE_LIST_lt': False}

    key_positions = []
    mode_lt = False
    for idx, token in enumerate(tokens):
        is_list_item = token in KEYS_LIST and mode_lt
        is_key = token in KEYS or is_list_item
        if is_key:
            key_positions.append(idx)
            if CANON.get(token, token) == 'lt':
                mode_lt = True
            elif token in KEYS:
                mode_lt = False

    for i, key_idx in enumerate(key_positions):
        token = tokens[key_idx]
        next_idx = key_positions[i + 1] if i + 1 < len(key_positions) else len(tokens)
        data = tokens[key_idx + 1:next_idx]

        if token in KEYS and CANON.get(token, token) != 'lt':
            context['MODE_LIST_lt'] = False

        formatted, context = format_output(token, data, context, fmt)
        if formatted:
            output.append(formatted)

        if CANON.get(token, token) == 'lt':
            context['MODE_LIST_lt'] = True

    return output

if __name__ == "__main__":
    if '--help' in sys.argv or '-h' in sys.argv:
        print(HELP)
        sys.exit(0)

    fmt = None
    if '-f' in sys.argv or '--format' in sys.argv:
        flag = '-f' if '-f' in sys.argv else '--format'
        idx = sys.argv.index(flag)
        if idx + 1 < len(sys.argv):
            fmt = sys.argv[idx + 1]
        else:
            print(f"Error: {flag} requires a format argument", file=sys.stderr)
            sys.exit(1)

    FORMATS = {
        'md': lambda tokens: "\n".join(process_tokens(tokens, 'md')),
    }

    if fmt is None:
        print("Error: -f, --format is required", file=sys.stderr)
        sys.exit(1)
    if fmt not in FORMATS:
        print(f"Error: unsupported format '{fmt}'. Supported: {', '.join(FORMATS)}", file=sys.stderr)
        sys.exit(1)

    tokens = tokenize_input(sys.stdin.read())
    print(FORMATS[fmt](tokens))
