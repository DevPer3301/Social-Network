from main import api
from models import Vote
from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime


class Analytics(Resource):
    @jwt_required()
    def get(self, start_date="2022-02-24", end_date="2022-02-28"):
        start_date = start_date.split("-")
        end_date = end_date.split("-")
        likes = 0
        votes = Vote.query.all()
        for vote in votes:
            if (vote.voted_at >= datetime(int(start_date[0]), int(start_date[1].lstrip("0")), int(start_date[2].lstrip("0")), 0, 0, 0, 000000)) and (vote.voted_at <= datetime(int(end_date[0]), int(end_date[1].lstrip("0")), int(end_date[2].lstrip("0")), 0, 0, 0, 000000)) and vote.vote == "Like":
                likes += 1
        return jsonify({"likes": likes})


api.add_resource(Analytics, '/api/analitics/date_from=<string:start_date>&date_to=<string:end_date>')




