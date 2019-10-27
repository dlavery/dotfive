def unpack_categories(cat, data):
    category = {'id': 'cat'+'.'+str(cat.id), 'text': cat.name, 'type': 'category'}
    children = []
    for c in cat.children:
        children = unpack_categories(c, children)
    for i in cat.items:
        children.append({'id': 'itm'+'.'+str(i.id), 'text': i.label})
    category['children'] = children
    data.append(category)
    return data
