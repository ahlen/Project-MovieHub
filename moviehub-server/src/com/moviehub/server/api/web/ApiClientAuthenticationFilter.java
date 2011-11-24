package com.moviehub.server.api.web;

import java.io.IOException;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;

public class ApiClientAuthenticationFilter implements Filter {

	@Override
	public void destroy() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void doFilter(ServletRequest req, ServletResponse res,
			FilterChain chain) throws IOException, ServletException {
		// TODO Auto-generated method stub
		
		
		
		if (req.getAttribute("test") != null && req.getParameter("test").equals("a")) {
			//res.getWriter().write("Det blev test");
			System.out.println("Fel");
			
			res.getWriter().write("Hello You");
			
			//throw new ServletException("Test");
			
		}
		
		chain.doFilter(req, res);
		
		System.out.println("executing ApiClientAuthenticationFilter");
	}

	@Override
	public void init(FilterConfig config) throws ServletException {
		// TODO Auto-generated method stub
		
	}

}
