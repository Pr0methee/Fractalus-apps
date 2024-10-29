import markdown
import tkinter.font as font

def add_markdown(markdown_text,text_widget):
    l=['']
    html = markdown.markdown(markdown_text)
    for elt in html:
        if elt == '<' and l[-1]== '' :
            l[-1]+=elt
        elif elt=='<' and l[-1][0]!='<':
            l.append(elt)
        elif elt=='<':raise
        elif elt == '>' and l[-1] != '' and l[-1][0]=='<':
            l[-1]+=elt
            l.append('')
        elif elt=='>':raise
        else:
            l[-1]+=elt
    while l[-1]=='':
        l.pop()

    i=0
    fnt = font.Font(family="Comic",size=12)
    fonts=[fnt]
    for elt in l:
        if elt not in ('<h1>','</h1>','<p>','<strong>','</strong>','</p>'):
            use=fonts[-1]
            new = use.copy()
            text_widget.tag_configure('tag'+str(i),font=use)
            fonts.append(new)
            text_widget.insert('end',elt,'tag'+str(i))
            i+=1
        else:
            match elt:
                case '<h1>':
                    fonts[-1].config(size=20)
                case '</h1>':
                    fonts[-1].config(size=12)
                case '<p>':
                    fonts[-1].config(size=12)
                    fonts[-1].config(weight='normal')
                    fonts[-1].config(slant='roman')
                case '<strong>':
                    fonts[-1].config(weight='bold')
                case '</strong>':
                    fonts[-1].config(weight='normal')
                case _:pass
