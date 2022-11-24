# CMPUT404-GroupProject

#### CMPUT 404

This repo is for the CMPUT 404 web group project

Our project is about Django web development, and our group members are

| Member Name | CCID   |
| ----------- | ------ |
| Wenhao Cao  | wcao4  |
| Kexun Niu   | kexun  |
| Ning Sun    | ning2  |
| Mengju Liao | mengju |
| Xuantong Ma         | xuantong    |

Project and Information are represent in WiKi


# API Reference

#### Library needed

```
  pip -install -r requirements.txt [or pip3, depends on your environment]
```

## Authors

**GET** URL: //service/authors
```authors
  To get all authors list.
```

**GET** URL: //service/authors?page={page_number}&size={size_number}
```
  To get all authors list of {size_number} authors displayed in a page and on page {page_number}

  Eg. GET ://service/authors?page=10&size=5, Gets the 5 authors, authors 45 to 49.
```

## Single Author

**GET** URL: //service/authors/{author_uuid}
```author
  To get the author {author_uuid}’s profile details.
```

**POST** URL: //service/authors?page={page_number}&size={size_number}
```
  Update the author’s profile details.

                    Eg. {
                        "type":"author",
                        # ID of the Author
                        "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                        # the home host of the author
                        "host":"http://127.0.0.1:5454/",
                        # the display name of the author
                        "displayName":"Lara Croft",
                        # url to the authors profile
                        "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                        # HATEOS url for Github API
                        "github": "http://github.com/laracroft",
                        # Image from a public domain
                        "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
                        }

```

## Posts

**GET** URL: //service/authors/{author_uuid}/posts/
```posts
  To get all posts of the author {author_uuid}.
```

**POST** URL: //service/authors/{author_uuid}/posts/
```
  To create a new post, with a new UUID

                            Eg.    {
                                        "type": "post",
                                        "title": "newPost",
                                        "description": "Charfield",
                                        "content": "Charfield",
                                        "Categories": "",
                                        "contentType": "text/plain",
                                        "textType": "text/plain",
                                        "count": 0,
                                        "published": "2022-11-22T23:05:44.157843Z",
                                        "visibility": "PUBLIC",
                                        "post_image": null,
                                        "unlisted": false,
                                        "author": "username"
                                    }

```

**GET** URL: //service/authors/{author_uuid}/posts/{post_uuid}
```posts
  GET get the public post whose id is {post_uuid}
```

**POST** URL: //service/authors/{author_uuid}/posts/{post_uuid}
```posts
  update the post whose id is {post_uuid} (must be authenticated , will be redirect to login page.)
```

**DELETE** URL: //service/authors/{author_uuid}/posts/{post_uuid}
```posts
  remove the post whose id is {post_uuid}
```

**DELETE** URL: //service/authors/{author_uuid}/posts/{post_uuid}
```posts
  create a post where its id is {post_uuid}
```


## Image Posts

**GET** URL: //service/authors/{author_uuid}/posts/{post_uuid}/image
```image_posts
  To get image of a post {post_uuid}. If no image file associate with, return 404. If so, display the image
```

## Comments

**GET** URL: //service/authors/{author_uuid}/posts/{post_uuid}/comments
```comments
  To get comments of a post {post_uuid}. If no comments associate with, return 404.
```

**POST** URL: //service/authors/{author_uuid}/posts/{post_uuid}/comments
```comments
  To create comments of a post {post_uuid}.
  
                          Eg. {
                                        "type": "comment",
                                        "author": "username",
                                        "comment": "comment content",
                                        "contentType":"text/plain"
                                    }
```


