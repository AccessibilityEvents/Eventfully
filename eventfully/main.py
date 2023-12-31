from flask import Flask, render_template, request, jsonify
from uuid import uuid4
from eventfully.categorize import get_topic
import eventfully.database as db

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html', events=list(db.Event.select().dicts()))


@app.route("/add_window", methods=["GET"])
def add_window():
    return render_template('add_window.html')


@app.route("/filter_setting", methods=["GET"])
def filter_setting():
    return render_template('filter_setting.html')


# @app.route("/api/events/search")
# def search_events():
#     print(request.args)
#     return "", 200


@app.route("/api/events/search", methods=["GET"])
def get_events():
    category = request.args.get("kategorie", "")
    therm = request.args.get("search", "")
    location = request.args.get("ort", "")
    # distance = request.args.get("distanz")

    # result = list(db.Event.select().where(
    #     (
    #         (db.Event.title ** f"{therm}%") |
    #         (db.Event.description ** f"%{therm}%")
    #     ) & (
    #         db.Event.tags ** f"%{category}%"
    #     ) & (
    #         db.Event.address ** f"%{location}%" |
    #         db.Event.city.name == location
    #     )
    # ).dicts())

    result = list(db.Event.select().where(
        (
                (db.Event.title ** f"{therm}%") |
                (db.Event.description ** f"%{therm}%")
        ) & (
                db.Event.tags ** f"%{category}%"
        )
    ).dicts())

    return render_template("api/events.html", events=result)


@app.route("/api/emails", methods=["GET"])
def emails():
    return jsonify(list(db.EMailContent.select().dicts()))


@app.route("/api/add_event", methods=["POST"])
def add_event():
    # TODO: validation
    # location = request.args.get("location", "")
    tag = get_topic(request.args.get("description", "") + request.args.get("title", ""))

    db.Event.create(
        id=uuid4(),
        title=request.args.get("title", "---"),
        description=request.args.get("description", "---"),
        link=request.args.get("link", "---"),
        price=request.args.get("price", "---"),
        tags=tag,
        start_date=request.args.get("start_date", "---"),
        end_date=request.args.get("end_date", "---"),
        age=request.args.get("age", "---"),
        accessibility=request.args.get("accessibility", "---"),
        location=None
    )

    return "", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
