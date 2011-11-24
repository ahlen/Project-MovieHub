package com.moviehub.server.api.web;

import java.util.ArrayList;

import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement(name="error")
public class JsonError {
	public String type;
	public String message;
	public ArrayList<String> categories;
	
	public JsonError() {
		
	}
	
	public JsonError(String type, String msg) {
		this.type = type;
		this.message = msg;
		
		this.categories = new ArrayList<String>();
		this.categories.add("Hej A");
		this.categories.add("Hej B");
	}
	
	public String getType() {
		return this.type;
	}
	
	public String getMessage() {
		return this.message;
	}
}