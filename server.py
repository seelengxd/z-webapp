import folium
import json
import os
import random
from collections import Counter
import branca.colormap as cm
from flask import Flask, render_template, session, request, redirect

#https://python-graph-gallery.com/313-bubble-map-with-folium/
#https://getbootstrap.com/docs/4.0/examples/sticky-footer-navbar/ yeet

with open('xyp.json') as f:
    data = json.load(f)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatever'

def generateMap(inp):
    counted = Counter(inp)
    m = folium.Map(
        location=[1.358272723057509, 103.81677298098423],
        tiles="Stamen Toner",
        zoom_start=11
        )
    colormap = cm.LinearColormap(colors=['blue', 'red'], vmin=min(counted.values()), vmax=max(counted.values()))
    m.add_child(colormap)
    for code, count in counted.items():
        print(code)
        if code in data:
            folium.Circle(
                location=data[code],
                radius=100+count/max(counted.values())*500,
                popup=f'{code} - {count}',
                color=colormap(count),
                fill=True,
                fill_color=colormap(count)
            ).add_to(m)
        else:
            print(code)
    
    return m


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        if 'k' not in session:
            session['k'] = random.randint(1, 100)
            return redirect('/random')
    
    else:
        file_data = request.files['file'].read().decode().split('\n')
        print(file_data)
        try:
            assert all(1 < int(i[:2]) <= 82 for i in file_data)
        except Exception as e:
            print(e)
            #handle error eventually later
            return redirect('/')

        m = generateMap([i[:2] for i in file_data])
            
        with open(os.path.join(os.getcwd(), 'templates', f'{session["k"]}.html'), 'w') as f:
            f.write(m._repr_html_())
    return render_template('index.html', res=f"{session['k']}.html")

@app.route('/random')
def randomMap():
    if 'k' not in session:
        session['k'] = random.randint(1, 100)

    m = generateMap([f'{random.randint(8, 82):0>2}' for _ in range(500)])
    with open(os.path.join(os.getcwd(), 'templates', f'{session["k"]}.html'), 'w') as f:
        print('ran')
        f.write(m._repr_html_())
        # pass
    return render_template('index.html', res=f"{session['k']}.html")

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.run()
