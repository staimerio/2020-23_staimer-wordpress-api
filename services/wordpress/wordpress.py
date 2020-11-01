"""Services for wordpress controller"""

# Retic
from retic import env, App as app

# Requests_oauthlib
from requests_oauthlib import OAuth1

# Requests
import requests

# Services
from retic.services.responses import error_response, success_response

# Constants
WP_POST_STATUS = app.config.get('WP_POST_STATUS')


class Wordpress(object):
    def __init__(
        self,
        oauth_consumer_key,
        oauth_consumer_secret,
        oauth_token,
        oauth_token_secret,
        base_url,
    ):
        """
        Create a wordpress instance
        """
        self.oauth_session = OAuth1(
            oauth_consumer_key,
            oauth_consumer_secret,
            oauth_token,
            oauth_token_secret,
        )

        self.url_api_base = base_url
        self.url_api_base_posts = self.url_api_base+"/posts"
        self.post_status = WP_POST_STATUS

    def create_resource(
        self,
        name,
        slug="",
        meta=None,
        resource="tags",
    ):
        """Define the metadata"""
        try:
            _metadata = {
                "name": str(name).lower(),
                "slug": slug,
                "meta": meta if meta else {}
            }
            """Prepare payload for the request"""
            _url = "{0}/{1}".format(
                self.url_api_base,
                resource
            )
            """Create the resource, if it has any problem, return None"""
            req_resource = requests.post(
                _url,
                auth=self.oauth_session,
                json=_metadata
            )
            """Return the data"""
            return req_resource.json()
        except Exception as e:
            return None

    def create_post(
        self,
        title,
        slug,
        content,
        excerpt,
        categories,
        tags,
        meta,
        date,
        props_resources,
    ):
        try:
            """Define all list"""
            _props_resources_ids = {}

            """Get and create the ids tag list, if it already exist, don't create it"""
            _tags_id = self.create_resources_from_list(tags, 'tags')

            """Get and create the ids category list, if it already exist, don't create it"""
            _categories_id = self.create_resources_from_list(
                categories, 'categories')

            if props_resources:
                for _props_resource in props_resources:
                    """Get and create the ids type list, if it already exist, don't create it"""
                    _resources_ids = self.create_resources_from_list(
                        _props_resource['items'], _props_resource['name']
                    )
                    _props_resources_ids = {
                        **_props_resources_ids,
                        _props_resource['name']: _resources_ids
                    }

            """Prepare payload request"""
            _payload = {
                "content": content,
                "title": title,
                "excerpt": excerpt,
                "status": self.post_status,
                "categories": _categories_id,
                "tags": _tags_id,

                "meta": meta,
                "slug": slug,
                # "date": date
                # Add ids list of resources
                ** _props_resources_ids,
            }
            """Create a new post"""
            _req_post = requests.post(
                self.url_api_base_posts,
                auth=self.oauth_session,
                json=_payload
            )
            """Return the created post"""
            return success_response(
                data=_req_post.json()
            )
        except Exception as err:
            return error_response(
                msg=str(err)
            )

    def update_post(
        self,
        post_id,
        data
    ):
        try:
            """Prepare payload"""
            _url = "{0}/{1}".format(self.url_api_base_posts, post_id)
            _payload = {
                **data
            }
            """Update a post"""
            _req_post = requests.post(
                _url,
                auth=self.oauth_session,
                json=_payload
            )
            """Return the created post"""
            return success_response(
                data=_req_post.json()
            )
        except Exception as err:
            return error_response(
                msg=str(err)
            )

    def get_post_by_id(
        self,
        post_id,
    ):
        try:
            """Prepare payload"""
            _url = "{0}/{1}".format(self.url_api_base_posts, post_id)
            """Update a post"""
            _req_post = requests.get(
                _url,
                auth=self.oauth_session,
            )
            """Return the created post"""
            return success_response(
                data=_req_post.json()
            )
        except Exception as err:
            return error_response(
                msg=str(err)
            )

    def create_resources_from_list(
        self,
        items,
        resource
    ):
        """Create resource in based a list

        : param items: List of items that you can created o find
        : param resource: Tag of the kind of resource
        """
        _items = []
        for _item in items:
            _value = self.create_resource(**_item, resource=resource)
            _items.append(
                _value['data']['term_id'] if (
                    "data" in _value) else _value['id']
            )
        return _items

    def get_post_by_slug(
        self,
        slug
    ):
        try:
            """Prepare payload"""
            _payload = {
                u"slug": slug
            }
            """Update a post"""
            _req_post = requests.get(
                self.url_api_base_posts,
                auth=self.oauth_session,
                params=_payload
            )
            """Check if it has results"""
            _posts = _req_post.json()
            if not _posts:
                raise Exception("Post not found")
            """Return the created post"""
            return success_response(
                data=_posts.pop()
            )
        except Exception as err:
            return error_response(
                msg=str(err)
            )
