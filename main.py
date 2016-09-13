#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class blog(db.Model):
    title = db.StringProperty(required = True)
    NewPost = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)



class MainHandler(webapp2.RequestHandler):

    def get(self):
        t = jinja_env.get_template("main_blog.html")
        response = t.render()
        self.response.write(response)

    def post(self):
        title = self.request.get("title")
        NewPost = self.request.get("NewPost")

        if title and NewPost:
            a = blog(title=title, NewPost=NewPost)
            a.put()
            NewPosts = db.GqlQuery("SELECT * FROM blog ORDER BY created DESC")

            t = jinja_env.get_template("new_post.html")
            response = t.render(title =title, NewPosts=NewPosts)
            self.response.write(response)

        else:
            error = "you need a title and a new post"
            t = jinja_env.get_template("main_blog.html")
            response = t.render(title =title, NewPost=NewPost,
                                error = error)
            self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
