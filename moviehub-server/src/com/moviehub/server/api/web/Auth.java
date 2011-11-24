package com.moviehub.server.api.web;

import java.io.IOException;
import java.util.List;

import javax.jdo.PersistenceManager;
import javax.jdo.Query;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;

import org.codehaus.jackson.JsonGenerationException;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.map.annotate.JsonRootName;
import org.codehaus.jettison.json.JSONArray;

import com.moviehub.server.api.PMF;
import com.moviehub.server.api.domain.Client;

@Path("/auth")
public class Auth {
	private ObjectMapper mapper = new ObjectMapper();
	
	public class AuthLoginMessage {
		private int status;
		private String message;
		
		public AuthLoginMessage(String message) {
			this.status = 200;
			this.message = message;
		}
		
		public int getStatus() {
			return this.status;
		}
		
		public String getMessage() {
			return this.message;
		}
	}
	
	@GET
	@Produces("application/json")
	public String auth() throws JsonGenerationException, JsonMappingException, IOException {
		
		AuthLoginMessage lgm = new AuthLoginMessage("Hello World");
		
		return mapper.writeValueAsString(lgm);
	}
	
	@GET
	@Produces("application/json")
	@Path("/error")
	public JsonError error() {
		JsonError err = new JsonError("TokenException", "Could not grant access by token");
		
		return err;
	}
	
	@GET
	@Produces("application/json")
	@Path("/add_data")
	public String addData() {
		Client c1 = new Client("Moviehub", "http://movie-hub.appspot.com");
		c1.generateSecret();
		
		PersistenceManager pm = PMF.get().getPersistenceManager();
		
		try {
			pm.makePersistent(c1);
		} finally {
			pm.close();
		}
		
		return "";
	}
	
	@GET
	@Produces("application/json")
	@Path("/get_data")
	public String getData() throws JsonGenerationException, JsonMappingException, IOException {
		
		Query query = PMF.get().getPersistenceManager().newQuery(Client.class);
		
		List<Client> clients;
		try {
			clients = (List<Client>)query.execute();			
		} finally {
			query.closeAll();
		}
		
		return mapper.writeValueAsString(clients);
	}
	
	
	
	/*@GET
	@Produces("text/plain")
	public String info(@QueryParam("test") String test) {
		if (test != null) {
			return "Hello " + test;
		} else {
			return "Test from Jersey";
		}
	}*/
}
