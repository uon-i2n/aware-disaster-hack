
import folium
from folium.plugins import Search
import herepy
import pandas as pd
from pandas.io.json import json_normalize 
import numpy as np
from ast import literal_eval
from folium.features import CustomIcon
from folium import IFrame

html_form = """

<h> Add your details here </h>

<ul>
<li>
<label class="description" for="element_1">Are you or anyone in your home likely to need assistance in an evacuation</label>
<span>
<input id="element_4_1" name="element_4" class="element radio" type="radio" value="1" />
<label class="choice" for="element_4_1">Yes</label>
<input id="element_4_2" name="element_4" class="element radio" type="radio" value="2" />
<label class="choice" for="element_4_2">No</label>
</span> 
</li>

<li>
<label class="description" for="element_5">Tick the items you have to assist in emergencies</label>
<span>
<input id="element_5_1" name="element_5_1" class="element checkbox" type="checkbox" value="1" />
<label class="choice" for="element_5_1">Pool</label>
<input id="element_5_2" name="element_5_2" class="element checkbox" type="checkbox" value="1" />
<label class="choice" for="element_5_2">Generator</label>
<input id="element_5_3" name="element_5_3" class="element checkbox" type="checkbox" value="1" />
<label class="choice" for="element_5_3">Bunker</label>
</span> 
</li>

<li>
<label class="description" for="element_5">Tick the languages you speak</label>
<span>
<input id="element_5_1" name="element_5_1" class="element checkbox" type="checkbox" value="1" />
<label class="choice" for="element_5_1">English</label>
<input id="element_5_2" name="element_5_2" class="element checkbox" type="checkbox" value="1" />
<label class="choice" for="element_5_2">Chinese</label>
<input id="element_5_3" name="element_5_3" class="element checkbox" type="checkbox" value="1" />
<label class="choice" for="element_5_3">Spanish</label>
</span> 
</li>

<li>
<label class="description" for="element_5">Tick the hazards in your area</label>
<span>
<input id="element_5_1" name="element_5_1" class="element checkbox" type="checkbox" value="1" />
<label class="choice" for="element_5_1">Bushland</label>
<input id="element_5_2" name="element_5_2" class="element checkbox" type="checkbox" value="1" />
<label class="choice" for="element_5_2">Fuel Storage</label>
<input id="element_5_3" name="element_5_3" class="element checkbox" type="checkbox" value="1" />
<label class="choice" for="element_5_3">Ammunitions</label>
</span> 
</li>

<li>
<label class="description" for="element_2">Any further details </label>
<div>
    <textarea id="element_2" name="element_2" class="element textarea medium"></textarea> 
</div>
</li>
</ul>
<p>
<button type="button" onclick="alert('You submitted!')">Submit!</button>
</p>"""

m = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles='Stamen Terrain')


app_id = 'kj5O3uIQcg0mzyy6Dyeb'

app_code = 'UYxM0q2BZXVoHqthopku6A'

geocoderApi = herepy.GeocoderApi(app_id, app_code)

placesApi = herepy.PlacesApi(app_id, app_code)

# response = placesApi.onebox_search([-25.2744,133.7751], 'pool')

m = folium.Map(location=[-25.2744,133.7751],
                zoom_start=4,
                tiles='Stamen Terrain')

def generate_layer(search_text,coords,colour):
    response = placesApi.onebox_search(coords, search_text)

    df = json_normalize(response.results,'items')

    layer = folium.FeatureGroup(name=search_text)

    for index,row in df.iterrows():
        pin_name = ''
        if('alternativeNames' in df):
            if(str(row['alternativeNames']) != 'nan'):
                name_dict = literal_eval(str(list(row['alternativeNames'])[0]))
                pin_name = name_dict['name']
        popup_desc = folium.Popup(str(pin_name),max_width=200,parse_html=True)
        icon_desc = folium.Icon(color=colour,icon='info-sign')
        layer.add_child(folium.Marker(location=row['position'],popup=popup_desc,icon=icon_desc))

    return layer

# iframe = IFrame(html=html_form, width=700, height=250)
# popup = folium.Popup(iframe, max_width=2650)
# folium.Marker([-15,133], popup=popup).add_to(m)


m.add_child(generate_layer('pools',[-25.2744,133.7751],'blue'))
m.add_child(generate_layer('restaurants',[-25.2744,133.7751],'green'))
m.add_child(generate_layer('hospital',[-25.2744,133.7751],'green'))
m.add_child(generate_layer('infrastructure',[-15.2744,133.7751],'black'))
m.add_child(generate_layer('supplies',[-35.2744,133.7751],'green'))
m.add_child(generate_layer('skills',[-25.2744,123.7751],'green'))
m.add_child(generate_layer('bunkers',[-25.2744,143.7751],'black'))
m.add_child(generate_layer('translators',[-25.2744,113.7751],'green'))
m.add_child(generate_layer('hazards',[-25.2744,133.7751],'red'))
m.add_child(generate_layer('meeting points',[-25.2744,133.7751],'blue'))
m.add_child(generate_layer('transport',[-25.2744,133.7751],'purple'))
m.add_child(generate_layer('vulnerabilities',[-25.2744,133.7751],'yellow'))

m.add_child(folium.LayerControl())
m.add_child(folium.ClickForMarker(popup='ADDED MARKER'))


m.save('map.html')
