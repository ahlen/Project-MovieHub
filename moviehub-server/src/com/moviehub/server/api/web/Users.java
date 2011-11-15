package com.moviehub.server.api.web;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;

@Path("/users")
public class Users {
	@GET
	@Produces("text/plain")
	public String info() {
		return "Test from Jersey";
	}
}
