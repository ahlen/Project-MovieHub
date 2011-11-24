package com.moviehub.server.api.domain;

import java.util.Date;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PrimaryKey;

import com.google.appengine.api.datastore.Key;

@PersistenceCapable
public class Client {
	
	@PrimaryKey
	@Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
	private Key key;
	
	@Persistent
	private String name;
	
	@Persistent
	private String secret;
	
	@Persistent
	private String redirectUri;

	@Persistent
	private Date createdAt;
	
	public Client(String name, String redirectUri) {
		this.name = name;
		this.redirectUri = redirectUri;
		this.createdAt = new Date();
		// TODO: generate secret
	}
	
	public Key getKey() {
		return this.key;
	}
	
	public String getName() {
		return this.name;
	}
	
	public String getSecret() {
		return this.secret;
	}
	
	public String getRedirectUri() {
		return this.redirectUri;
	}
	
	public Date getCreatedAt() {
		return this.createdAt;
	}
	
	public void setName(String name) {
		this.name = name;
	}
	
	/*public void setSecret(String secret) {
		this.secret = secret;
	}*/
	
	public void setRedirectUri(String redirectUri) {
		this.redirectUri = redirectUri;
	}
	
	public void setCreatedAt(Date date) {
		this.createdAt = date;
	}
	
	public void generateSecret() {
		// TODO: generate secret
	}
}