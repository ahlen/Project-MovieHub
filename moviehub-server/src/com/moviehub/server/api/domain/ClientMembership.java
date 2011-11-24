package com.moviehub.server.api.domain;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PrimaryKey;

import com.google.appengine.api.datastore.Key;

/*
 * Client membership which handle the relationship
 * between users and trusted 3rd party clients/apps
 * 
 * Because the use of Big Table in Google App Engine
 * we can't and should not use "joins" in a RMDS
 * way, instead we should use something called
 * "Relation Index Entity" described
 * http://dl.google.com/io/2009/pres/W_0415_Building_Scalable_Complex_App_Engines.pdf
 *  
 *  
 */
@PersistenceCapable
public class ClientMembership {
	
	@Persistent
	@PrimaryKey
	private Key key;
	
	@Persistent
	private Client client;
	
	@Persistent
	private String token;
	
	public ClientMembership(Client client) {
		this.client = client;
	}
	
	public void generateToken() throws NoSuchAlgorithmException {
		MessageDigest digest = MessageDigest.getInstance("SHA-128");
		//this.token = new String(digest.digest(TODO: add data here));
	}
}