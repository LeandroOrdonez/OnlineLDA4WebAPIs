def new_term(term_id, term):
    return """<Term rdf:about="http://www.example.org/terms/%s">
    <has_content rdf:datatype="http://www.w3.org/2001/XMLSchema#string">%s</has_content>
    </Term>""" % (term_id, term)

def new_membership_relation(membership_relation_id, membership_probability, category_value):
    return """<Membership_Relation rdf:about="http://www.example.org/membership_relations/%s">
    <membership_probability rdf:datatype="http://www.w3.org/2001/XMLSchema#double">%.4f</membership_probability>
    <category_value rdf:resource="http://www.example.org/categories/%s"/>
    </Membership_Relation>""" % (membership_relation_id, membership_probability, category_value)

def new_operation(operation_id, membership_relations):
    memberships = ''.join(['<is_member_of rdf:resource="http://www.example.org/membership_relations/%s"/>\n' \
% `membership` for membership in membership_relations])
    return """<Operation rdf:about="http://www.example.org/operations/%s">
    %s  
    </Operation>""" % (operation_id, memberships)

def new_term_relation(term_relation_id, term_probability, term_value):
    return """<Term_Relation rdf:about="http://www.example.org/term_relations/%s">
    <term_probability rdf:datatype="http://www.w3.org/2001/XMLSchema#double">%.4f</term_probability>
    <term_value rdf:resource="http://www.example.org/terms/%s"/>
    </Term_Relation>""" % (term_relation_id, term_probability, term_value)

def new_category(category_id, term_relations):
    terms = ''.join(['<has_term rdf:resource="http://www.example.org/term_relations/%s"/>\n' \
% `term` for term in term_relations])
    return """<Category rdf:about="http://www.example.org/categories/%s">
    %s  
    </Category>""" % (category_id, terms)
