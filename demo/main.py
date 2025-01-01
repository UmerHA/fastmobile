from fastmobile import *

app, rt = fast_app()

red = '#FF4847'
light_grey, muted_grey, dark_grey = '#E1E1E1', '#8D9494', '#4E4D4D'
blue = '#4778FF'
txt_style = dict(fontFamily='Roboto', fontSize=16, lineHeight=24)
bold_txt_style = dict(fontWeight='bold', **txt_style)

styles = Styles(
    Style('FormGroup', margin='l24 r24 t24'),
    Style('Input', borderBottomColor=light_grey, borderBottomWidth=1, borderColor=dark_grey, padding='b8 t8', **txt_style)(
        WhenFocused(borderBottomColor=blue)),
    Style('Label', borderColor=dark_grey, margin='b8', **bold_txt_style),
    Style('Text', **txt_style),
    Style('Help', borderColor=red, margin='t16', **txt_style),
    Style('Input--Error', borderBottomColor=red, color=red)(
        WhenFocused(borderBottomColor=red)),
    Style('Help--Error', color=red),
    Style('Submit', color=blue, margin='t16', **bold_txt_style),
    Style('NextBtn', color='white', backgroundColor=blue, borderRadius=6, padding=6, margin=24, **bold_txt_style)),

def mk_form(err=False):
    def maybe_err(o): return f'{o} {o}--Error' if err else o
    return Form(_id='myForm', style='FormGroup')(
        Text(f'What\'s tastier? Mango or apple?', style='Label'),
        TextField(name='fruit', style=maybe_err('Input'),
            placeholder='Placeholder', placeholderTextColor=muted_grey),
        Text(f'Enter mango or apple' if err else 'Follow your heart', style=maybe_err('Help')),
        Text('Submit', style='Submit', href='/submit', verb='get', target='myForm', action='replace', show_during_load='mySpinner'))

@rt('/screen1')
def get():
    return Doc(Screen(
        styles,
        Body(
            mk_form(),
            Spinner(_id='mySpinner', hide='true'))))

@rt('/screen2')
def get():
    return Doc(Screen(
        styles,
        Body(
            View(style='FormGroup')(
                Text('Your taste is surpreme', style='Label')))))

@rt('/index')
def get():
    return Doc(StackNav(NavRoute(_id='screen1', href='/screen1')))

@rt('/submit1')
def get(fruit:str):
    valid   = fruit.lower() in ['mango','apple']
    correct = fruit.lower() == 'mango'
    if valid:
        view = View(style='FormGroup')(
                Text('What\'s tastier? Mango or apple?', style='Label'),
                Text('Your answer: '+fruit, style='Text'),
                Text('Correct!' if correct else 'Objectively wrong', style='Submit'))
        if correct:
            view = View(
                view,
                Text('Let\'s continue', style='NextBtn', href='/screen2')
            )
        return view
    else:
        return mk_form(err=True)

if __name__ == "__main__": serve(port=8085)
