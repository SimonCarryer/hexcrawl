import sys
import random
from flask import Flask, jsonify, redirect, url_for, request, render_template
from hex import Map

app = Flask(__name__)

app.config['map'] = Map()

def hex_context():
    context = app.config['map'].look()
    encounters = app.config['map'].get_encounter_set()
    directions = app.config['map'].valid_directions()
    return render_template('hex.html', context=context, directions=directions, encounters=encounters)

def explore_context(place):
    context = place.explore()
    return_coords = '.'.join([str(i) for i in app.config['map'].current_hex.coords])
    return render_template('explore.html', context=context, return_coords=return_coords)

@app.route('/')
def api_root():
    return redirect('/hex/0.0')

@app.route("/travel/<direction>", methods=['POST'])
def move(direction):
    app.config['map'].change_current_hex(direction)
    coords = '.'.join([str(i) for i in app.config['map'].current_hex.coords])
    return redirect('/hex/%s' % coords)

@app.route("/hex/<coords>")
def hex(coords):
    coords = [int(i) for i in coords.split('.')]
    app.config['map'].current_hex = app.config['map'].get_hex_by_coords(coords)
    return hex_context()

@app.route("/explore/<place>")
def explore(place):
    place = app.config['map'].current_hex.places[place]
    return explore_context(place)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)