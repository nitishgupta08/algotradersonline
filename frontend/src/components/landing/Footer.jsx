import React, { useState } from "react";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import EmailIcon from "@mui/icons-material/Email";
import InfoIcon from '@mui/icons-material/Info';
import GitHubIcon from '@mui/icons-material/GitHub';
import Divider from '@mui/material/Divider';
import {
  Tooltip,
  Box,
  Typography,
  Grid,
  IconButton,
  Backdrop,
} from "@mui/material";
import TOC from "./TOC";

function Footer() {
  const [open, setOpen] = useState(false);
  const [about,setAbout] = useState(false);

  return (
    <Box component="footer" sx={{ display: "flex", mt: 2 }}>
      <Backdrop
        sx={{
          color: "#fff",
          zIndex: (theme) => theme.zIndex.drawer + 1,
          backdropFilter: "blur(4px)",
        }}
        open={open}
        onClick={() => setOpen(false)}>
        <TOC />
      </Backdrop>
       <Backdrop
        sx={{
          color: "#fff",
          zIndex: (theme) => theme.zIndex.drawer + 1,
          backdropFilter: "blur(4px)",
        }}
        open={about}
        onClick={() => setAbout(false)}>
        <About />
      </Backdrop>
      <Grid container>
        <Grid item xs={6}>
          <Box component="section">
              <Typography
                  variant="h1"
                  sx={{
                      fontSize: "2rem",
                      fontWeight: 600,
                  }}>
                  algotradersonline.com
              </Typography>
            <Typography variant="subtitle1" sx={{ fontSize: "1rem" }}>
              Automate your trade with us
            </Typography>

            <Box sx={{ display: "flex" }}>
              <Typography
                variant="subtitle2"
                sx={{
                  mt: 10,
                  mr: 1,
                  mb: 2,
                  cursor: "pointer",
                  color: "primary.main",
                }}
                onClick={() => setOpen(true)}>
                Terms and Conditions
              </Typography>
              <Typography variant="subtitle2" sx={{ mt: 10, ml: 1, mb: 2 }}>
                &copy; All rights reserved
              </Typography>
            </Box>
          </Box>
        </Grid>
        <Grid item xs={6}>
          <Box
            component="section"
            sx={{ display: "flex", justifyContent: "end", alignItems: "center" }}>

             <Tooltip title="About" placement="top">
              <IconButton
                sx={{ color: "primary.main" }}
                onClick={() => setAbout(true)}>
                <InfoIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Mail" placement="top">
              <IconButton
                sx={{ color: "primary.main" }}
                onClick={() =>
                  window.open("mailto:mukesh.algotraders@gmail.com")
                }>
                <EmailIcon />
              </IconButton>
            </Tooltip>

            <Tooltip title="Address" placement="top">
              <IconButton
                sx={{ color: "primary.main" }}
                onClick={() =>
                  window.open(
                    "https://www.google.com/maps/dir//The+LNM+Institute+of+Information+Technology,+Rupa+ki+Nangal,+Post-Sumel,+Via-Jamdoli+Jaipur-302031,,+Goner+Rd,+Dher+Ki+Dhani,+Jaipur,+Rajasthan+303012/@26.8972824,75.8696902,13z/data=!4m9!4m8!1m0!1m5!1m1!1s0x396db71d58ddb54d:0xe64f31eae498f069!2m2!1d75.8941993!2d26.8572442!3e0",
                    "_blank",
                    "noreferrer"
                  )
                }>
                <LocationOnIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Footer;

const About = () => {
  const a = "https://avatars.dicebear.com/api/bottts/anupam-nagpal.svg";
  const n = "https://avatars.dicebear.com/api/bottts/Nitish-kumar-gupta.svg";
  const s = "https://avatars.dicebear.com/api/bottts/sanyam-lodha.svg";
  const t = "https://avatars.dicebear.com/api/bottts/Tanmaylodha.svg";

  return(
     <Box
      component="section"
      sx={{
        bgcolor: "background.paper",
        color: "text.primary",
        p: 3,
        borderRadius: 3,
      }}>
      <Box sx={{display:"flex", justifyContent:"center"}}>
        <Typography sx={{ fontSize: "2rem", fontWeight: 600 }}>
          Developers
        </Typography>
      </Box>
      <Divider sx={{m:1}}/>
      <Box sx={{m:2, display:"flex",alignItems:"center"}}>
        <Box
              component="img"
              src={a}
              alt="profile"
              sx={{
                height: "75px",
                width: "75px",
                backgroundColor: "black",
                borderRadius: 50,
                boxShadow: "1px 0px 20px 10px rgba(0,0,0,0.1)",
                p:0.5,
              }}
            />
        <Box sx={{display:"flex", flexDirection:"column", alignItems:"start",ml:2}}>
        <Typography sx={{ fontSize: "1.2rem", fontWeight: 600 }}>
          Anupam Nagpal
        </Typography>
          <IconButton
            sx={{ mt: 0.5, p: 0 }}
            onClick={() =>
              window.open(
                "https://github.com/Anupam0107",
                "_blank",
                "noreferrer"
              )
            }>
            <GitHubIcon sx={{ color:"text.primary"}} />
          </IconButton>
        </Box>
      </Box>
      <Box sx={{ m: 2, display: "flex", alignItems: "center" }}>
           <Box
              component="img"
              src={n}
              alt="profile"
              sx={{
                height: "75px",
                width: "75px",
                backgroundColor: "black",
                borderRadius: 50,
                boxShadow: "1px 0px 20px 10px rgba(0,0,0,0.1)",
                p:0.5,
              }}
            />
        <Box sx={{ display: "flex", flexDirection: "column", alignItems: "start", ml: 2 }}>
          <Typography sx={{ fontSize: "1.2rem", fontWeight: 600 }}>
            Nitish Kumar Gupta
          </Typography>
          <IconButton
          sx={{mt:0.5,p:0}}
            onClick={() =>
              window.open(
                "https://github.com/nitishgupta08",
                "_blank",
                "noreferrer"
              )
            }>
            <GitHubIcon sx={{ color: "text.primary" }} />
          </IconButton>
        </Box>
        </Box>
      <Box sx={{ m: 2, display: "flex", alignItems: "center" }}>
          <Box
              component="img"
              src={s}
              alt="profile"
              sx={{
                height: "75px",
                width: "75px",
                backgroundColor: "black",
                borderRadius: 50,
                boxShadow: "1px 0px 20px 10px rgba(0,0,0,0.1)",
                p:0.5,
              }}
            />
        <Box sx={{ display: "flex", flexDirection: "column", alignItems: "start", ml: 2 }}>
          <Typography sx={{ fontSize: "1.2rem", fontWeight: 600 }}>
            Sanyam Lodha
          </Typography>
          <IconButton
            sx={{ mt: 0.5, p: 0 }}
            onClick={() =>
              window.open(
                "https://github.com/Sanyam0908",
                "_blank",
                "noreferrer"
              )
            }>
            <GitHubIcon sx={{ color: "text.primary" }} />
          </IconButton>
        </Box>
        </Box>
      <Box sx={{ m: 2, display: "flex", alignItems: "center" }}>
           <Box
              component="img"
              src={t}
              alt="profile"
              sx={{
                height: "75px",
                width: "75px",
                backgroundColor: "black",
                borderRadius: 50,
                boxShadow: "1px 0px 20px 10px rgba(0,0,0,0.1)",    
                p:0.5,
              }}
            />
        <Box sx={{ display: "flex", flexDirection: "column", alignItems: "start", ml: 2 }}>
          <Typography sx={{ fontSize: "1.2rem", fontWeight: 600 }}>
            Tanmay Lodha
          </Typography>
          <IconButton
            sx={{ mt: 0.5, p: 0 }}
            onClick={() =>
              window.open(
                "https://github.com/TanmayLodha",
                "_blank",
                "noreferrer"
              )
            }>
            <GitHubIcon sx={{ color: "text.primary" }} />
          </IconButton>
        </Box>
        </Box>
 
    </Box>
  );
}
