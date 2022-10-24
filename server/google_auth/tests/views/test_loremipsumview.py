import pytest
from django.contrib.auth.models import User

PROFILE_ENDPOINT = "/api/lorem_ipsum/"


@pytest.mark.django_db
def test_successful_authentication(auth_client):
    """
    Test when test user can successfully login,
    protected endpoint can be accessed.
    """

    response = auth_client.get(PROFILE_ENDPOINT, format="json")

    expected_response = {
        "title": "Lorem Ipsum",
        "paragraph": """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut sed risus a ante euismod laoreet. Vestibulum vel congue ipsum. Proin tempus leo nunc. Nulla pellentesque porta tortor vitae tempus. Phasellus porttitor lacus sit amet lobortis dictum. In vel gravida augue, et vulputate purus. Fusce eu nulla sed velit ultrices pellentesque. Donec imperdiet purus orci, id vehicula ex elementum in. Ut nec neque a dolor semper pellentesque. In consectetur sapien a tortor blandit, ut cursus enim placerat. Duis ac quam sed nulla commodo ultrices. Phasellus laoreet convallis arcu, ut pulvinar nunc ornare a. Duis nec nulla in magna maximus pulvinar ut vitae tellus.

            Nam faucibus tincidunt mauris, et ultricies ipsum sollicitudin at. Fusce sapien lectus, porttitor id sapien vel, rhoncus varius orci. Sed a quam at urna fringilla dictum vel eget nulla. Duis tincidunt maximus efficitur. Nulla ultricies quam lectus, ac condimentum nunc ultrices quis. Maecenas lacinia semper sapien dictum pellentesque. Mauris tincidunt tempus neque, sit amet suscipit tortor convallis a. Vestibulum mattis metus et lacus blandit, sit amet viverra ligula finibus. Sed placerat tincidunt tortor quis eleifend. Nulla condimentum volutpat urna a tristique.

            Nullam congue non leo eu vehicula. Pellentesque finibus lobortis elit, eu auctor tortor cursus in. Quisque mattis id lorem eget aliquet. Suspendisse placerat lorem sed quam posuere bibendum. Sed vulputate sit amet est ac blandit. Mauris vehicula nisl sed lectus aliquet tristique. Aliquam venenatis ultrices imperdiet. Praesent sagittis sagittis ligula, sed porttitor lorem posuere in. Aenean convallis dui nisi, non rhoncus nulla condimentum a. Vestibulum aliquet arcu id magna efficitur placerat. Nam tempor accumsan ligula, hendrerit scelerisque erat molestie eu. Praesent eget hendrerit risus.

            Donec tortor massa, interdum in ligula in, dapibus placerat est. Etiam ac lectus sapien. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Duis ut orci rutrum, porttitor nibh a, auctor nisl. In eget ultrices mi. Nam erat purus, varius eget porttitor vel, tempus eget justo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Proin eu posuere odio. Pellentesque ante urna, gravida facilisis sagittis non, semper nec tortor.

            Donec id euismod orci, quis consectetur massa. Fusce sed purus non risus dignissim elementum at suscipit arcu. Donec tincidunt lacus a mi pulvinar, et volutpat odio efficitur. Sed ullamcorper et ex vitae iaculis. Integer id iaculis tortor. Phasellus suscipit elit neque, sit amet mollis velit sollicitudin vel. Nunc feugiat iaculis arcu, ac venenatis est lacinia ac. In felis metus, volutpat eu nibh nec, vulputate viverra nisl. Praesent sollicitudin iaculis sem, in sollicitudin odio tristique at. Aenean eu elementum nibh, a gravida neque. Sed vestibulum magna turpis, nec suscipit dolor ultricies vel. In feugiat leo lacus, eu cursus nisi commodo at.
            """,
    }

    assert response.status_code == 200
    assert response.data == expected_response
