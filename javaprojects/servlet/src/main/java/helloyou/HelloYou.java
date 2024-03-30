package helloyou;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class HelloYou
 */
@WebServlet("/HelloYou")
public class HelloYou extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public HelloYou() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.setContentType("text/html");
		String nome = request.getParameter("nome");	
		PrintWriter out = response.getWriter();		
		out.println("<!doctype html>");
		out.println("<html>");
		out.println("<head>");
		out.println("<title>Hello World Sample Servlet</title>");
		out.println("</head>");
		out.println("<body>");
		out.println("<center><h1>Hello "+ nome +" </h1></center>");
		out.println("</body>");
		out.println("</html>");
		out.close();
	}

}
