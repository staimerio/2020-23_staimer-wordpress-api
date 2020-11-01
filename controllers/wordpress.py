# Retic
from retic import Request, Response, Next

# Services
from services.wordpress import wordpress
from retic.services.validations import validate_obligate_fields
from retic.services.responses import success_response, error_response


def create_post(req: Request, res: Response, next: Next):
    """Create a new post"""

    """Validate obligate params"""
    _validate = validate_obligate_fields({
        u'title': req.param('title'),
        u'oauth_consumer_key': req.headers.get('oauth_consumer_key'),
        u'oauth_consumer_secret': req.headers.get('oauth_consumer_secret'),
        u'oauth_token': req.headers.get('oauth_token'),
        u'oauth_token_secret': req.headers.get('oauth_token_secret'),
        u'base_url': req.headers.get('base_url'),
    })

    """Check if has errors return a error response"""
    if _validate["valid"] is False:
        return res.bad_request(
            error_response(
                "{} is necesary.".format(_validate["error"])
            )
        )

    _wordpress_instance = wordpress.Wordpress(
        req.headers.get('oauth_consumer_key'),
        req.headers.get('oauth_consumer_secret'),
        req.headers.get('oauth_token'),
        req.headers.get('oauth_token_secret'),
        req.headers.get('base_url'),
    )
    _post = _wordpress_instance.create_post(
        title=req.param('title'),
        slug=req.param('slug', None),
        content=req.param('content', ""),
        excerpt=req.param('excerpt', ""),
        categories=req.param('categories', []),
        tags=req.param('tags', []),
        meta=req.param('meta', {}),
        date=req.param('date', ""),
        # Add others params
        props_resources=req.param('props_resources', []),
    )

    """Check if it has any problem"""
    if _post['valid'] is False:
        res.bad_request(_post)
    else:
        res.ok(_post)


def update_post(req: Request, res: Response, next: Next):
    """Update a post"""

    """Validate obligate params"""
    _validate = validate_obligate_fields({
        u'post_id': req.param('post_id'),
        u'data': req.param('data'),
        u'oauth_consumer_key': req.headers.get('oauth_consumer_key'),
        u'oauth_consumer_secret': req.headers.get('oauth_consumer_secret'),
        u'oauth_token': req.headers.get('oauth_token'),
        u'oauth_token_secret': req.headers.get('oauth_token_secret'),
        u'base_url': req.headers.get('base_url'),
    })

    """Check if has errors return a error response"""
    if _validate["valid"] is False:
        return res.bad_request(
            error_response(
                "{} is necesary.".format(_validate["error"])
            )
        )

    _wordpress_instance = wordpress.Wordpress(
        req.headers.get('oauth_consumer_key'),
        req.headers.get('oauth_consumer_secret'),
        req.headers.get('oauth_token'),
        req.headers.get('oauth_token_secret'),
        req.headers.get('base_url'),
    )

    _post = _wordpress_instance.update_post(
        post_id=req.param('post_id'),
        data=req.param('data'),
    )

    """Check if it has any problem"""
    if _post['valid'] is False:
        res.bad_request(_post)
    else:
        res.ok(
            success_response(
                data=_post['data'],
                msg="Post updated."
            )
        )


def get_post_by_id(req: Request, res: Response, next: Next):
    """Validate obligate params"""
    _validate = validate_obligate_fields({
        u'oauth_consumer_key': req.headers.get('oauth_consumer_key'),
        u'oauth_consumer_secret': req.headers.get('oauth_consumer_secret'),
        u'oauth_token': req.headers.get('oauth_token'),
        u'oauth_token_secret': req.headers.get('oauth_token_secret'),
        u'base_url': req.headers.get('base_url'),
    })

    """Check if has errors return a error response"""
    if _validate["valid"] is False:
        return res.bad_request(
            error_response(
                "{} is necesary.".format(_validate["error"])
            )
        )

    _wordpress_instance = wordpress.Wordpress(
        req.headers.get('oauth_consumer_key'),
        req.headers.get('oauth_consumer_secret'),
        req.headers.get('oauth_token'),
        req.headers.get('oauth_token_secret'),
        req.headers.get('base_url'),
    )
    """Get a post"""

    _post = _wordpress_instance.get_post_by_id(
        post_id=req.param('post_id'),
    )

    """Check if it has any problem"""
    if _post['valid'] is False:
        res.bad_request(_post)
    else:
        res.ok(
            success_response(
                data=_post['data'],
                msg='Post found.'
            )
        )


def get_all_search(req: Request, res: Response):
    if req.param('slug'):
        return get_by_slug(req, res)
    return res.bad_request("Bad request")


def get_by_slug(req: Request, res: Response):
    """Validate obligate params"""
    _validate = validate_obligate_fields({
        u'oauth_consumer_key': req.headers.get('oauth_consumer_key'),
        u'oauth_consumer_secret': req.headers.get('oauth_consumer_secret'),
        u'oauth_token': req.headers.get('oauth_token'),
        u'oauth_token_secret': req.headers.get('oauth_token_secret'),
        u'base_url': req.headers.get('base_url'),
    })

    """Check if has errors return a error response"""
    if _validate["valid"] is False:
        return res.bad_request(
            error_response(
                "{} is necesary.".format(_validate["error"])
            )
        )

    _wordpress_instance = wordpress.Wordpress(
        req.headers.get('oauth_consumer_key'),
        req.headers.get('oauth_consumer_secret'),
        req.headers.get('oauth_token'),
        req.headers.get('oauth_token_secret'),
        req.headers.get('base_url'),
    )

    """Get all novel from latests page"""
    _post = _wordpress_instance.get_post_by_slug(
        slug=req.param('slug')
    )
    """Check if exist an error"""
    if _post['valid'] is False:
        return res.not_found(_post)
    else:
        """Response the data to client"""
        res.ok(
            success_response(
                data=_post['data'],
                msg='Post found.'
            )
        )
