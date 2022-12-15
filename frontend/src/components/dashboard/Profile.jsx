import React, { useContext, useState, useEffect } from "react";
import { UserContext } from "../../UserContext";
import {
    Box,
    Typography,
    Button,
    Card,
    TextField,
    Divider,
    Snackbar,
    Alert, Grid,
} from "@mui/material";
import AccountBoxIcon from "@mui/icons-material/AccountBox";
import SecurityIcon from "@mui/icons-material/Security";
import { BaseURL } from "../../BaseURL";
// https://avatars.dicebear.com/api/:sprites/:seed.svg

function Profile({ img }) {
  const { user } = useContext(UserContext);
  const current = JSON.parse(user);
  const [isDesktop, setDesktop] = useState(window.innerWidth <= 1200);
  const [password, setPassword] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });
  const [passerror, setPasserror] = useState(false);
  const [error, setError] = useState(false);

  const [open, setOpen] = useState(false);
  const updateMedia = () => {
    setDesktop(window.innerWidth <= 1200);
  };

  useEffect(() => {
    window.addEventListener("resize", updateMedia);
    return () => window.removeEventListener("resize", updateMedia);
  });

  const validatePassword = (e) => {
    setPassword({ ...password, confirmPassword: e.target.value });
    if (e.target.value !== password.newPassword) {
      setPasserror(true);
    } else {
      setPasserror(false);
    }
  };

  const handleChangePassword = (e) => {
    e.preventDefault();
    if (passerror) {
      setError(true);
      return;
    }

    const credentials = {
      old_password: password.currentPassword,
      new_password: password.newPassword,
    };

    fetch(BaseURL + "api/change-password/", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${current.data.token}`,
      },
      body: JSON.stringify(credentials),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("error");
        } else {
          return response.json();
        }
      })
      .then((data) => {
        setOpen(true);
        console.log(data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const snackBarClose = () => {
    setOpen(false);
  };
  const errorClose = () => {
    setError(false);
  };

  return (
    <>
      <Snackbar
        open={open}
        autoHideDuration={5000}
        onClose={snackBarClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "left" }}>
        <Alert severity="success" variant="filled">
          Password Successfully Changed
        </Alert>
      </Snackbar>
      <Snackbar
        open={error}
        autoHideDuration={5000}
        onClose={errorClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "left" }}>
        <Alert severity="error" variant="filled">
          Fields don't match. Check again
        </Alert>
      </Snackbar>
      <Box
        sx={{
          width: isDesktop ? "50vw" : "30vw",
          p: 2,
          transition: " all .15s ease-in-out",
          backgroundColor: "background.default",
          height: "100vh",
        }}>
        <Box sx={{ m: 1, mb: 3, display: "flex", justifyContent: "center" }}>
          <Typography
            variant="h1"
            style={{ wordWrap: "break-word" }}
            sx={{
              fontSize: "2rem",
              fontWeight: 600,
              mt: 1,
            }}>
            Profile
          </Typography>
        </Box>
        <Card
          sx={{
            display: "flex",
            flexDirection: "column",
            borderRadius: 3,
            boxShadow: "0px 0px 10px 5px rgba(0,0,0,0.1)",
            transition: " all .15s ease-in-out",
            p: 5,
          }}>
          <Box sx={{ display: "flex", alignItems: "center" }}>
            <AccountBoxIcon sx={{ mb: 1, opacity: 0.8 }} />
            <Typography
              variant="h1"
              style={{ wordWrap: "break-word" }}
              sx={{
                fontSize: "1.3rem",
                fontWeight: 600,
                mb: 1,
                ml: 1,
                opacity: 0.8,
              }}>
              ACCOUNT
            </Typography>
          </Box>
          <Divider />
            <Grid container spacing={2}>
                <Grid item xs={3}>
                    <Box
                        component="img"
                        src={img}
                        alt="profile"
                        sx={{
                            height: "100px",
                            width: "100px",
                            backgroundColor: "black",
                            borderRadius: 50,
                            mt:2,
                            boxShadow: "1px 0px 20px 10px rgba(0,0,0,0.1)",
                        }}
                    />
                </Grid>
                <Grid item xs='auto'>
                    <Box>
                        <Typography
                            variant="h1"
                            sx={{ fontSize: "2.5rem", fontWeight: 600 }}>
                            {current.data.username}
                        </Typography>
                        <Typography
                            variant="h1"
                            style={{ wordWrap: "break-word" }}
                            sx={{
                                fontSize: "1.5rem",
                                fontWeight: 500,
                                mt: 1,
                            }}>
                            {current.data.email}
                        </Typography>
                        <Typography
                            variant="h1"
                            sx={{
                                fontSize: "1rem",
                                fontWeight: 500,

                                display: "inline-block",
                            }}>
                            AliceblueID:
                        </Typography>
                        <Typography
                            variant="h1"
                            sx={{
                                fontSize: "1.3rem",
                                fontWeight: 600,
                                ml: 1,
                                display: "inline-block",
                            }}>
                            {current.data.aliceBlueID}
                        </Typography>
                    </Box>
                </Grid>
            </Grid>
        </Card>

        <Card
          sx={{
            display: "flex",
            flexDirection: "column",
            borderRadius: 3,
            boxShadow: "0px 0px 10px 5px rgba(0,0,0,0.1)",
            transition: " all .15s ease-in-out",
            p: 5,
            mt: 2,
          }}>
          <Box sx={{ display: "flex", alignItems: "center" }}>
            <SecurityIcon sx={{ mb: 1, opacity: 0.8 }} />
            <Typography
              variant="h1"
              style={{ wordWrap: "break-word" }}
              sx={{
                fontSize: "1.3rem",
                fontWeight: 600,
                mb: 1,
                ml: 1,
                opacity: 0.8,
              }}>
              SECURITY
            </Typography>
          </Box>
          <Divider />
          <Box sx={{ mt: 2 }}>
            <TextField
              name="password"
              required
              label="Current Password"
              type="password"
              fullWidth
              value={password.currentPassword}
              onChange={(e) =>
                setPassword({ ...password, currentPassword: e.target.value })
              }
              sx={{ mt: 1 }}
            />
            <TextField
              name="password"
              required
              label="New Password"
              type="password"
              fullWidth
              value={password.newPassword}
              onChange={(e) =>
                setPassword({ ...password, newPassword: e.target.value })
              }
              sx={{ mt: 3 }}
            />
            <TextField
              name="password"
              required
              label="Confirm Password"
              type="password"
              fullWidth
              error={passerror}
              value={password.confirmPassword}
              onChange={validatePassword}
              sx={{ mt: 3 }}
            />
            <Button
              type="submit"
              variant="contained"
              onClick={handleChangePassword}
              sx={{ mt: 5, width: "100%" }}>
              Change Password
            </Button>
          </Box>
        </Card>
      </Box>
    </>
  );
}

export default Profile;
