from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from aaolm.portlet.coverphoto import CoverPhotoPortletMessageFactory as _

# custom additions below
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName


class ICoverPhotoPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ICoverPhotoPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Cover Photo Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        context = aq_inner(self.context)

    def show(self):
        """Only render if we're viewing a Smart Folder and that the 
        current folder contains our cover image (cover.jpg) 
        OR we're in the portal root viewing a Topic.
        """
        context = aq_inner(self.context)
        portal_url = getToolByName(context, "portal_url").getPortalObject().absolute_url()
        print '\n\n\n <---------- HERE I AM THIS IS ME! ---------->\n' + portal_url + ' ' + context.absolute_url() + '\n'
        if context.portal_type == 'Topic' and (
                    'cover.jpg' in context.aq_inner.getParentNode().contentIds() 
                    or 
                    context.absolute_url() in [portal_url, portal_url+'/index.html', portal_url+'/index.htm']
                    ):
            return True
        return False
    
    def latest_cover_image(self):
        """Query the portal catalog and return the newest cover.jpg that
        exists w/in the portal at the given location.  If we're at the root,
        the script will return the newest cover.jpg for the entire site.  If
        we're viewing an issue, it should only query the portal catalog from
        that folder or subfolder and will return the latest cover.jpg 
        contained in that folder.
        NOTE: this method only gets called when we're viewing a Topic that either
        has a cover.jpg at the same level as the Topic or we're viewing a Topic
        at the root of our site.
        """

        context = aq_inner(self.context)
        portal_catalog = getToolByName(context, 'portal_catalog')
        cover_image = portal_catalog(id='cover.jpg', 
                                     portal_type='Image',
                                     sort_on='effective',
                                     sort_order='reverse',
                                     path='/'.join(context.getPhysicalPath()).replace('/index.html', ''),
                                     )
        return cover_image[0].getObject().absolute_url()

    #cover = 'cover.jpg'
    #cover_large = cover + '/image_view_fullscreen'
    #cover_small = cover + '/image_mini'
    Title = 'Magazine Cover'
    
    render = ViewPageTemplateFile('coverphotoportlet.pt')

class AddForm(base.NullAddForm):
    """Portlet add form.
    """
    def create(self):
        return Assignment()

