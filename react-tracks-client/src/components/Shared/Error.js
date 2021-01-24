import React, { useState } from "react";
import withStyles from "@material-ui/core/styles/withStyles";
import Button from "@material-ui/core/Button";
import Snackbar from "@material-ui/core/Snackbar";

const Error = ({ classes, error }) => {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <Snackbar 
      open={ isOpen }
      className={ classes.snackbar }
      message={ error.message }
      action={
        <Button color="secondary" size="small" onClick={ () => setIsOpen(false) }><b>Close</b></Button>
      }
    />
  )
};

const styles = theme => ({
  snackbar: {
    margin: theme.spacing.unit
  }
});

export default withStyles(styles)(Error);
