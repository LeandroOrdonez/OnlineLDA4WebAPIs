import urllib
import httplib2

class SesameHandler:

    def __init__(self, repository='WebAPIModel', sesame_server='http://localhost:8080/openrdf-sesame/', \
namespace='http://www.example.org/web-api-model.rdf', resource='statements'):
        """
	Documentation...
        """
        self.endpoint='%srepositories/%s/%s' % (sesame_server, repository, resource)
        self.rdf_wrap="""<rdf:RDF
xmlns=\""""+namespace+"""#"
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
xml:base=\""""+namespace+"""">
%s
</rdf:RDF>"""

    def post_statement(self, rdf_encoded_data):
        print 'POSTing statement to %s' % (self.endpoint)
        data = self.rdf_wrap % (rdf_encoded_data)
        headers= {
            'content-type': 'application/rdf+xml;charset=UTF-8'
        }
        (response, content) = httplib2.Http().request(self.endpoint, 'POST', body=data, headers=headers)
        print 'Response %s' % response.status
        print content
