/*
 * File: scripts.js
 * Description: Client-side form field validation.
 * Date: 2014/04/27
 * Programmer: Thomas Newman
 */

/*
 * Chart Functions
 */

// Creates a pie chart for categories.
function drawPieChart(canvas_element, category_names, category_values)
{
    // Original concept:
    // https://developer.apple.com/library/safari/documentation/AudioVideo/Conceptual/HTML-canvas-guide/CreatingChartsandGraphs/CreatingChartsandGraphs.html
    
    var category_total = 0;
    
    for (var i = 0; i < category_values.length; i++)
    {
        category_total += category_values[i];
    }
    
    canvas_context = canvas_element.getContext("2d");
    canvas_context.lineWidth = 2;
    canvas_context.fillStyle="#005b89";
    canvas_context.strokeStyle = "white";
    
    var x_midpoint = canvas_element.width / 2;
    var y_midpoint = canvas_element.height / 2;
    var radius = Math.min(x_midpoint, y_midpoint) * 0.70;
    var starting_point = 0;
    var text_angle = 0;
    var text_x_distance = 0;
    var text_y_distance = 0;
    var text_x_start = 0;
    var text_y_start = 0;
    var label = "";
    
    for (var i = 0; i < category_values.length; i++)
    {
        slice_size = category_values[i] / category_total;
        slice_angle = (slice_size * 2 * Math.PI)
        ending_point = starting_point + slice_angle;
        
        // Draw Slice
        canvas_context.beginPath();
        canvas_context.arc(x_midpoint, y_midpoint, radius, starting_point, ending_point);
        canvas_context.lineTo(x_midpoint, y_midpoint);
        canvas_context.closePath();
        canvas_context.fill();
        canvas_context.stroke();
        
        // Draw Label
        text_angle = starting_point + (slice_angle / 2);
        text_x_start = x_midpoint + radius * Math.cos(text_angle) * 1.05;
        text_y_start = y_midpoint + radius * Math.sin(text_angle) * 1.05;
        
        canvas_context.font = "bold 10px Arial";
        canvas_context.fillStyle = "#005b89";
        label = category_names[i] + " (" + (slice_size * 100).toFixed(0) + "%)";
        
        // Quadrant IV
        if (text_angle >= 0 && text_angle < (Math.PI / 2))
        {
            canvas_context.textAlign = "left";
            canvas_context.textBaseline="top";
        }
        // Quadrant III
        else if (text_angle >= (Math.PI / 2) && text_angle < Math.PI)
        {
            canvas_context.textAlign = "right";
            canvas_context.textBaseline="top";
        }
        // Quadrant II
        else if (text_angle >= Math.PI && text_angle < (3 * Math.PI / 2))
        {
            canvas_context.textAlign = "right";
            canvas_context.textBaseline="bottom";
        }
        // Quadrant I
        else if (text_angle >= (3 * Math.PI / 2) && text_angle < (2 * Math.PI))
        {
            canvas_context.textAlign = "left";
            canvas_context.textBaseline="bottom";
        }
        
        canvas_context.fillText(label, text_x_start, text_y_start);
        
        starting_point = ending_point;
    }
}

/*
 * Wire event handlers on page load
 */

// Adds event handlers to a page
function init()
{
	navigationInit();
	validationInit();
	logoutInit();
	deleteInit();
}

/*
 * Event handlers for page navigation
 */

// Adds the onchange event that activates the prompt for unsaved changes 
// event handler when each form element is modified.
function navigationInit()
{
	var form = document.getElementById("form");
	
	// Only bother processing form elements if the form element exists
	
	if(form != null)
	{
		// Set the onchange event for all form inputs to trigger a prompt when the 
		// user navigates away from the page
		var formElements = new Array();
		var inputElements = document.getElementsByTagName("input");
		var selectElements = document.getElementsByTagName("select");
		var textElements = document.getElementsByTagName("textarea");
		
		// For input tags, filter the submission button
		for(var i = 0; i < inputElements.length; i++)
		{
			var currentElement = inputElements[i];
		
			if(currentElement.type != "submit")
			{
				formElements.push(currentElement);
			}
		}
		
		// For all other tags, there is no filtering
		for(var i = 0; i < selectElements.length; i++)
		{
			var currentElement = selectElements[i];
		
			formElements.push(currentElement);
		}
		
		for(var i = 0; i < textElements.length; i++)
		{
			var currentElement = textElements[i];
		
			formElements.push(currentElement);
		}
		
		for(var i = 0; i < formElements.length; i++)
		{
			var currentElement = formElements[i];
			
			currentElement.onchange = setUnsetChanges;
		}
		
		// Clear the prompt on navigate if the user is submitting the form	
		form.onsubmit = clearUnsetChanges;
	}
}

// Informs the user that unsaved changes will be lost and asks the user 
// to confirm navigation.
function promptUnsavedChanges()
{
	return "Unsaved changes will be lost if you navigate away from this page.";
}

// Adds the prompt unsaved changes event when the page is reloaded/a 
// new page is loaded.
function setUnsetChanges()
{
	window.onbeforeunload = promptUnsavedChanges;
}

// Removes the prompt unsaved changes event when the page is reloaded/a new page is loaded.
function clearUnsetChanges()
{
	window.onbeforeunload = null;
}

// Adds event handlers for the logout event.
function logoutInit()
{
	var logoutElement = document.getElementById("logout");
	
	if(logoutElement != null)
	{
		logoutElement.onclick = promptLogout;
	}
}

// Prompts the user to confirm logout.
function promptLogout()
{
	return confirm("Are you sure you want to log out?");
}

// Adds event handlers for the delete event.
function deleteInit()
{
	var deleteElement = document.getElementById("delete");
	
	// Some pages don't have a delete link
	if(deleteElement != null)
	{
		deleteElement.onclick = promptDelete;
	}
}

// Prompts the user to confirm deletion.
function promptDelete()
{
	return confirm("Are you sure you want to delete this entry?");
}

/*
 * Input Validation
 */

// Adds onblur event handlers to the form elements that exist on this 
// page and have validation logic.
function validationInit()
{
	var nameField = document.getElementById("name");
	var briefDescriptionField = document.getElementById("briefdescription");
	var descriptionField = document.getElementById("description");
	var dueDateField = document.getElementById("duedate");
	var usernameField = document.getElementById("username");
	var passwordField = document.getElementById("password");
	var submitField = document.getElementById("submit");
	
	if(nameField != null)
	{
		nameField.onblur = validateName;
	}
	
	if(briefDescriptionField != null)
	{
		briefDescriptionField.onblur = validateBriefDescription;
	}
	
	if(descriptionField != null)
	{
		descriptionField.onblur = validateDescription;
	}
	
	if(dueDateField != null)
	{
		dueDateField.onblur = validateDueDate;
	}
	
	if(usernameField != null)
	{
		usernameField.onblur = validateusername;
	}
	
	if(passwordField != null)
	{
		passwordField.onblur = validatePassword;
	}
	
	if(submitField != null)
	{
		submitField.onclick = validateFields;
	}
}

// Validates all form fields requiring validation. Returns true if all 
// of the fields there were found on the page validated, otherwise false 
// is returned.
function validateFields()
{
	var nameField = document.getElementById("name");
	var briefDescriptionField = document.getElementById("briefdescription");
	var descriptionField = document.getElementById("description");
	var dueDateField = document.getElementById("duedate");
	var usernameField = document.getElementById("username");
	var passwordField = document.getElementById("password");
	var validFields = true;
	
	// Only validate the name field if it exists on the page
	if(nameField != null)
	{
		if(!validateName())
		{
			validFields = false;
		}
	}
	
    // Only validate the brief description field if it exists on the page
	if(briefDescriptionField != null)
	{
		if(!validateBriefDescription())
		{
			validFields = false;
		}
	}
	
    // Only validate the description field if it exists on the page
	if(descriptionField != null)
	{
		if(!validateDescription())
		{
			validFields = false;
		}
	}
	
    // Only validate the due date field if it exists on the page
	if(dueDateField != null)
	{
		if(!validateDueDate())
		{
			validFields = false;
		}
	}
	
	if(usernameField != null)
	{
		if(!validateusername())
		{
			validFields = false;
		}
	}
	
    // Only validate the username field if it exists on the page
	if(passwordField != null)
	{
		if(!validatePassword())
		{
			validFields = false;
		}
	}
	
	return validFields;
}

// Validates the name field
function validateName()
{
	var nameField = document.getElementById("name");
	var errorDiv = document.getElementById("nameerror");
	
	// Blank Field Check
	if(isFieldBlank(nameField))
	{
		errorDiv.innerHTML = "Name cannot be blank!";
		return false;
	}
    
    // Length Check
    if(!shortFieldLengthCheck(nameField))
    {
        errorDiv.innerHTML = "Names are limited to a length of 50 characters!";
        return false;
    }
	
	errorDiv.innerHTML = "";
	return true;
}

// Validates the brief description field
function validateBriefDescription()
{
	var briefDescriptionField = document.getElementById("briefdescription");
	var errorDiv = document.getElementById("briefdescriptionerror");
	
	// Blank Field Check
	if(isFieldBlank(briefDescriptionField))
	{
		errorDiv.innerHTML = "Brief Description cannot be blank!";
		return false;
	}
    
    // Length Check
    if(!shortFieldLengthCheck(briefDescriptionField))
    {
        errorDiv.innerHTML = "Brief descriptions are limited to a length of 50 characters!";
        return false;
    }
	
	errorDiv.innerHTML = "";
	return true;
}

// Validates the description field
function validateDescription()
{
	var descriptionField = document.getElementById("description");
	var errorDiv = document.getElementById("descriptionerror");
	
	// Blank Field Check
	if(isFieldBlank(descriptionField))
	{
		errorDiv.innerHTML = "Description cannot be blank!";
		return false;
	}
    
    // Length Check
    if(!longFieldLengthCheck(descriptionField))
    {
        errorDiv.innerHTML = "Descriptions are limited to a length of 1000 characters!";
        return false;
    }
	
	errorDiv.innerHTML = "";
	return true;
}

// Validates the due date field
function validateDueDate()
{
	var dueDateField = document.getElementById("duedate");
	var errorDiv = document.getElementById("duedateerror");
	
	// Blank Field Check
	if(isFieldBlank(dueDateField))
	{
		errorDiv.innerHTML = "Due Date cannot be blank!";
		return false;
	}
	else if(!isFieldDate(dueDateField))
	{
		errorDiv.innerHTML = "Due Date must be in the form YYYY-MM-DD";
		return false;
	}
	
	errorDiv.innerHTML = "";
	return true;
}

function validateusername()
{
	var usernameField = document.getElementById("username");
	var errorDiv = document.getElementById("usernameerror");
	
	// Blank Field Check
	if(isFieldBlank(usernameField))
	{
		errorDiv.innerHTML = "Username cannot be blank!";
		return false;
	}
	
	errorDiv.innerHTML = "";
	return true;
}

function validatePassword()
{
	var passwordField = document.getElementById("password");
	var errorDiv = document.getElementById("passworderror");
	
	// Blank Field Check
	if(isFieldBlank(passwordField))
	{
		errorDiv.innerHTML = "Password cannot be blank!";
		return false;
	}
	
	errorDiv.innerHTML = "";
	return true;
}

/*
 * Input Validation Helper Functions
 */
 
// Checks if the provided element is blank
function isFieldBlank(element)
{
	if(element.value.length == 0)
	{
		return true;
	}

	return false;
}

// Checks if the provided element contains a valid date
function isFieldDate(element)
{
	var dateStr = element.value;
	var datePieces = dateStr.split("-");
	
	// A date must consist of 3 parts: Month/Day/Year
	if(datePieces.length != 3)
	{
		return false;
	}
	
	// Each Piece Must Be An Integer
	for(var index in datePieces)
	{
		var piece = datePieces[index];
	
		// Do Not Allow Floating Points
		if(piece.indexOf(".") != -1)
		{
			return false;
		}
		
		if(parseInt(piece) == NaN)
		{
			return false;
		}
	}
	
	var year = datePieces[0];
    var month = datePieces[1];
    var day = datePieces[2];
	
	// There are 12 months in a year
	if((month < 1) || (month > 12))
	{
		return false;
	}
	
	// Months With 30 Days (April, June, September, November)
	if((month == 4) || (month == 6) || (month == 9) || (month == 11))
	{
		if((day < 1) || (day > 30))
		{
			return false;
		}
	}
	// February
	else if(month == 2)
	{
		var maxDays = 0;
		
		if(isLeapYear(year))
		{
			maxDays = 29;
		}
		else
		{
			maxDays = 28;
		}
		
		if((day < 1) || (day > maxDays))
		{
			return false;
		}
	}
	// Months With 31 Days
	else
	{
		if(day < 1 || day > 31)
		{
			return false;
		}
	}
	
	// Years Must Be Positive
	if(year < 1)
	{
		return false;
	}
	
	return true;
}

// Checks if the element's input is within the limits for long fields. 
// Returns true if the field is within bounds, otherwise false is returned.
function shortFieldLengthCheck(element)
{
    if(element.value.length <= 50)
    {
        return true;
    }
    
    return false;
}

// Checks if the element's input is within limits for long fields.
// Returns true if the field is within bounds, otherwise false is returned.
function longFieldLengthCheck(element)
{
    if(element.value.length <= 1000)
    {
        return true;
    }
    
    return false;
}

// Checks if a given year is a leap year
function isLeapYear(year)
{
	// http://stackoverflow.com/questions/725098/leap-year-calculation 
    // provides a good leap year algorithm
	if((year % 4) == 0)
	{
		if((year % 100) != 0)
		{
			return true;
		}
	}
	
	if((year % 400) == 0)
	{
		return true;
	}
	
	return false;
}