# Vercel Speed Insights Setup Guide

This document explains how Vercel Speed Insights has been configured for this Streamlit application.

## What Was Implemented

Vercel Speed Insights tracking has been added to the `streamlit_app.py` file using the vanilla JavaScript approach. The tracking scripts are injected into every page through the `get_theme_css()` function, which is called on every page load.

### Code Changes

Added the following Speed Insights initialization scripts to `streamlit_app.py`:

```javascript
<script>
  window.si = window.si || function () { (window.siq = window.siq || []).push(arguments); };
</script>
<script defer src="/_vercel/speed-insights/script.js"></script>
```

These scripts are injected via Streamlit's `unsafe_allow_html=True` feature in the theme CSS function.

## Required Vercel Dashboard Configuration

**IMPORTANT:** For Speed Insights to work, you MUST complete these steps in the Vercel dashboard:

### Step 1: Enable Speed Insights

1. Log in to your Vercel dashboard at https://vercel.com
2. Navigate to your project (jameswol-ai/random)
3. Go to the "Speed Insights" tab in the sidebar
4. Click the "Enable" button
5. This will automatically add the `/_vercel/speed-insights/*` routes to your project

### Step 2: Deploy Your Application

After enabling Speed Insights:
1. Deploy your application to Vercel (either via Git push or `vercel deploy`)
2. The Speed Insights routes will be activated after the first deployment following enablement
3. The `/_vercel/speed-insights/script.js` endpoint will now be available

### Step 3: Verify Installation

After deployment:
1. Visit your deployed application
2. Open browser DevTools (F12)
3. Go to the Network tab
4. Look for a request to `/_vercel/speed-insights/script.js`
5. If the script loads successfully (200 status), Speed Insights is working

You can also check the Speed Insights dashboard in Vercel after some users visit your site.

## How It Works

1. **Script Initialization**: The first script creates a queue (`window.siq`) that collects any tracking calls before the main script loads
2. **Async Loading**: The second script loads the main Speed Insights tracking library asynchronously (using `defer`)
3. **Automatic Tracking**: Once loaded, Speed Insights automatically tracks:
   - Core Web Vitals (LCP, FID, CLS)
   - First Contentful Paint (FCP)
   - Time to First Byte (TTFB)
   - And other performance metrics

4. **Data Collection**: Performance data is sent to Vercel's servers at `/_vercel/speed-insights/vitals`
5. **Dashboard Visualization**: View collected metrics in the Vercel Speed Insights dashboard

## Framework Compatibility

This implementation uses the **vanilla JavaScript approach** which is:
- ✅ Framework-agnostic (works with any web application)
- ✅ No npm packages required
- ✅ Compatible with Streamlit's HTML injection
- ✅ Lightweight and non-blocking (uses `defer`)

## Limitations

- Speed Insights only works when the application is deployed on Vercel
- Local development (localhost) will show 404 errors for the script - this is expected
- You must enable Speed Insights in the Vercel dashboard before it will work
- The `/_vercel/speed-insights/` routes are only available after enabling the feature

## Testing

To test the implementation:

1. Ensure the application is deployed to Vercel
2. Ensure Speed Insights is enabled in the Vercel dashboard
3. Visit your deployed application
4. Wait for some users to visit (or visit yourself)
5. Check the Speed Insights dashboard in Vercel (may take a few minutes to show data)

## Troubleshooting

**Script not loading (404 error)**:
- Verify Speed Insights is enabled in Vercel dashboard
- Ensure you've deployed after enabling the feature
- Check that you're testing on the deployed site, not localhost

**No data in dashboard**:
- Wait at least 10-15 minutes after first visits
- Ensure your site has received actual user traffic
- Check browser console for any JavaScript errors
- Verify the script is loading successfully in Network tab

**Script loading but no metrics**:
- Some ad blockers may block analytics scripts
- Check that the vitals endpoint (`/_vercel/speed-insights/vitals`) is accessible
- Ensure your browser supports the required Web APIs

## Resources

- [Vercel Speed Insights Documentation](https://vercel.com/docs/speed-insights/quickstart)
- [Vercel Speed Insights Package](https://vercel.com/docs/speed-insights/package)
- [Web Vitals Explained](https://web.dev/vitals/)

## Support

For issues with Speed Insights:
- Check Vercel's documentation: https://vercel.com/docs/speed-insights
- Contact Vercel support through your dashboard
- Visit Vercel Community: https://community.vercel.com
