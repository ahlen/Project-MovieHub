package com.moviehub.server.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.View;

@Controller
@RequestMapping("/api/demos")
public class DemoController {
	public class DemoObject {
		private int id;
		private String name;
		
		public DemoObject(int id, String name) {
			this.id = id;
			this.name = name;
		}
		
		public int getId() {
			return this.id;
		}
		
		public String getName() {
			return this.name;
		}
	}
	
	@RequestMapping(method = RequestMethod.GET)
	public @ResponseBody DemoObject index() {
		DemoObject obj = new DemoObject(5, "Mikael");
		return obj;
	}
	
	@RequestMapping(value="new", method=RequestMethod.GET)
	public String create() {
		return "index";
	}
}
