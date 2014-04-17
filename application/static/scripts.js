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

// Validates all form fields requiring validation
function validateFields()
{
	var nameField = document.getElementById("name");
	var briefDescriptionField = document.getElementById("briefdescription");
	var descriptionField = document.getElementById("description");
	var dueDateField = document.getElementById("duedate");
	var usernameField = document.getElementById("username");
	var passwordField = document.getElementById("password");
	var validFields = true;
	
	// Only validate the fields that exist on this page
	if(nameField != null)
	{
		if(!validateName())
		{
			validFields = false;
		}
	}
	
	if(briefDescriptionField != null)
	{
		if(!validateBriefDescription())
		{
			validFields = false;
		}
	}
	
	if(descriptionField != null)
	{
		if(!validateDescription())
		{
			validFields = false;
		}
	}
	
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
		errorDiv.innerHTML = "Due Date must be in the form MM/DD/YYYY";
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
	var datePieces = dateStr.split("/");
	
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
	
	var month = datePieces[0];
	var day = datePieces[1];
	var year = datePieces[2];
	
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