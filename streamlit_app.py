# ============================================================
# RANDOM – AI Architectural Design Studio
# (Standards: Metric Handbook, Architectural Graphic Standards)
# Fully merged & error‑fixed – Evolution, Diagnostics, 2D/3D, Elevations, Room Editor
# ============================================================
import streamlit as st, json, uuid, random, hashlib, math
from pathlib import Path
from datetime import datetime
import pandas as pd, plotly.graph_objects as go, plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import io, numpy as np, base64, struct

# ---------- CONFIG ----------
st.set_page_config(page_title="RANDOM Studio", page_icon="⚡", layout="wide")
DATA_DIR = Path("data"); DATA_DIR.mkdir(exist_ok=True)
USER_FILE = DATA_DIR / "users.json"
FONT = ImageFont.load_default()
XP_PER_LEVEL = 100

# ---------- THEME ----------
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html,body,.stApp{background:radial-gradient(circle at top,#0a0f14,#05080c);font-family:'Inter',sans-serif;color:#e0e5eb}
h1,h2,h3,h4,h5,h6{font-weight:600;color:#f0f4f8;letter-spacing:-0.5px}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0f1319,#080b10);border-right:1px solid #2a2f38;box-shadow:inset -4px 0 12px rgba(0,0,0,0.3)}
.logo-text{font-size:2.4rem;font-weight:700;background:linear-gradient(135deg,#fbbf24,#f97316);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.5rem}
.stButton>button{background:linear-gradient(135deg,#fbbf24,#f97316);color:#0f172a;border:none;border-radius:14px;padding:0.7rem 2rem;font-weight:600;transition:all 0.3s;box-shadow:0 6px 20px rgba(251,191,36,0.25)}
.stButton>button:hover{transform:translateY(-2px);box-shadow:0 12px 30px rgba(251,191,36,0.4)}
.xp-container{display:flex;align-items:center;gap:10px;margin-bottom:1.2rem}
.xp-bar-bg{flex:1;height:10px;background:#1e293b;border-radius:6px;overflow:hidden}
.xp-bar-fill{height:100%;background:linear-gradient(90deg,#fbbf24,#f97316);border-radius:6px;box-shadow:0 0 10px #f97316}
.footer{text-align:center;padding:1.5rem 0;color:#5f6b7a;font-size:0.8rem;border-top:1px solid #2a2f38}
</style>""",unsafe_allow_html=True)

# ---------- AUTH ----------
def hash_password(pw): return hashlib.sha256((pw+"rand_salt").encode()).hexdigest()
def load_users():
    if USER_FILE.exists():
        try:
            with open(USER_FILE) as f: return json.load(f)
        except: return []
    return []
def save_users(users):
    with open(USER_FILE,"w") as f: json.dump(users,f,indent=2)
def get_user(uname):
    for u in load_users():
        if u["username"]==uname: return u
    return None
def create_user(uname,pw,role="user"):
    users=load_users()
    if get_user(uname): raise ValueError("Username exists")
    user={"username":uname,"password_hash":hash_password(pw),"role":role,"level":1,"xp":0,"badges":[],"created":datetime.now().isoformat()}
    users.append(user); save_users(users)
    return user
def authenticate(uname,pw):
    u=get_user(uname)
    if u and u["password_hash"]==hash_password(pw): return u
    return None
def update_user_data(uname,updates):
    users=load_users()
    for u in users:
        if u["username"]==uname: u.update(updates); break
    save_users(users)
def xp_for_level(lvl): return lvl*XP_PER_LEVEL
def add_xp(uname,amount):
    u=get_user(uname)
    if not u: return False
    old=u["level"]; u["xp"]+=amount
    while u["xp"]>=xp_for_level(u["level"]):
        u["xp"]-=xp_for_level(u["level"]); u["level"]+=1
        if u["level"]%5==0 and f"level_{u['level']}" not in u["badges"]:
            u["badges"].append(f"level_{u['level']}")
    update_user_data(uname,{"level":u["level"],"xp":u["xp"],"badges":u["badges"]})
    return u["level"]>old

# ---------- MEMORY ----------
def get_memory_path(uname): return DATA_DIR/f"{uname}_memory.json"
DEFAULT_MEMORY={"projects":[],"saved_designs":[],"logs":[]}
def load_memory(uname):
    path=get_memory_path(uname)
    if path.exists():
        try:
            with open(path,encoding="utf-8") as f: data=json.load(f)
            for k in DEFAULT_MEMORY:
                if k not in data: data[k]=DEFAULT_MEMORY[k]
            return data
        except: return DEFAULT_MEMORY.copy()
    return DEFAULT_MEMORY.copy()
def save_memory(uname,mem):
    with open(get_memory_path(uname),"w",encoding="utf-8") as f: json.dump(mem,f,indent=4)

# ---------- STANDARDS ----------
METRIC_STANDARDS = {
    "residential": {"ceil_height":2.4,"bedroom":12,"living":20,"kitchen":10,"bathroom":5,"dining":12,"study":9,"corridor_width":1.2},
    "commercial": {"ceil_height":3.0,"office":12,"meeting":15,"reception":12,"kitchen":15,"bathroom":6,"corridor_width":1.5},
    "industrial": {"ceil_height":4.0,"hall":50,"storage":30,"office":12,"bathroom":6,"corridor_width":2.0}
}
IMPERIAL_FACTOR = 10.7639

# ---------- UNIT CONVERTER ----------
def format_area(val, unit_sys="Metric"):
    if unit_sys=="Imperial": return f"{val*IMPERIAL_FACTOR:.0f} ft²"
    return f"{val:.1f} m²"
def format_length(val, unit_sys="Metric"):
    if unit_sys=="Imperial": return f"{val*3.28084:.1f} ft"
    return f"{val:.2f} m"

# ---------- ARCHITECTURE TYPES ----------
ARCH_TYPES = {
    "Residential": ["Luxury Villa","Modern Apartment","Townhouse"],
    "Commercial": ["Boutique Office","Corporate Hub","Hotel Resort","Medical Clinic"],
    "Industrial": ["Distribution Warehouse","Manufacturing Facility"]
}
def get_domain(name):
    for d,items in ARCH_TYPES.items():
        if name in items: return d.lower()
    return "commercial"

FLOORING_OPTS = ["tiles","wood","concrete","carpet","marble"]
CEILING_OPTS = ["flat","hanging","vaulted","exposed","coffered"]

# ---------- DESIGN GENERATOR ----------
def create_floor(level, building_type, total_area, modules, floor_area, n_rooms, enforce):
    domain = get_domain(building_type)
    std = METRIC_STANDARDS[domain]
    ceil_height = std["ceil_height"]
    if floor_area is None: floor_area = total_area/(modules*0.5+1)
    side = int(math.sqrt(floor_area))+1
    w = max(6, min(side, 30))
    d = max(6, min(side, 30))
    w = max(4, round(w/1.2)*1.2)
    d = max(4, round(d/1.2)*1.2)

    ess = {"residential":["living","kitchen","bathroom"],"commercial":["office","bathroom","corridor"],"industrial":["hall","bathroom","storage"]}
    if n_rooms>2 and "corridor" not in ess[domain]:
        ess[domain].append("corridor")
    rtypes = ess[domain] + random.choices(
        ["bedroom","study","dining","meeting","reception","office"],
        k=max(0, n_rooms - len(ess[domain]))
    )
    rtypes = rtypes[:n_rooms]

    typical_depth = d if d<10 else 6
    widths = []
    for rt in rtypes:
        min_area = std.get(rt, 10) if rt in std else 10
        if rt == "corridor": req_width = std["corridor_width"]
        else: req_width = max(2.0, min_area / typical_depth)
        widths.append(req_width)
    total_req = sum(widths)
    available_width = w - 0.2 * len(rtypes)
    if total_req > available_width:
        scale = available_width / total_req
        widths = [ww*scale for ww in widths]
    else:
        extra = (available_width - total_req) / len(rtypes)
        widths = [ww+extra for ww in widths]

    rooms = []
    x0 = 0.0
    for i, rt in enumerate(rtypes):
        rw = widths[i]
        if rw < 1.5: continue
        poly = [(x0,0),(x0+rw,0),(x0+rw,d),(x0,d)]
        door_type = "main" if rt in ["living","office","meeting","reception"] else "interior"
        if rt=="bathroom": door_type="bathroom"
        openings = [{"type":"door","wall":"north","width":0.9,"door_type":door_type,"adjacent":None}]
        if rt not in ("corridor","bathroom","storage"):
            win_w = min(rw*0.6, 2.0)
            openings.append({"type":"window","wall":"south","width":win_w})
        room = {
            "name": f"{rt.capitalize()} {i+1}",
            "type": rt,
            "polygon": poly,
            "openings": openings,
            "flooring": random.choice(FLOORING_OPTS),
            "ceiling": random.choice(CEILING_OPTS),
            "ceiling_height": ceil_height
        }
        rooms.append(room)
        x0 += rw

    walls = _create_walls(w,d)
    int_walls = []
    cur_x = 0
    for room in rooms:
        if cur_x > 0:
            int_walls.append({"start":(cur_x,0),"end":(cur_x,d),"thickness":0.2})
        cur_x += room["polygon"][1][0] - room["polygon"][0][0]
    walls.extend(int_walls)
    cols = _place_columns(w,d)
    beams = _place_beams(w,d)
    return {"level":level,"height":ceil_height,"rooms":rooms,"walls":walls,"columns":cols,"beams":beams,"slab":{"thickness":0.2}}

def _create_walls(w,d):
    return [{"start":(0,0),"end":(w,0),"thickness":0.3},{"start":(w,0),"end":(w,d),"thickness":0.3},
            {"start":(w,d),"end":(0,d),"thickness":0.3},{"start":(0,d),"end":(0,0),"thickness":0.3}]
def _place_columns(w,d):
    cols=[{"center":(0,0),"size":0.3,"shape":"square"},{"center":(w,0),"size":0.3,"shape":"square"},
          {"center":(0,d),"size":0.3,"shape":"square"},{"center":(w,d),"size":0.3,"shape":"square"}]
    for x in np.arange(4,w,4):
        for y in np.arange(4,d,4):
            if x<w-0.5 and y<d-0.5: cols.append({"center":(x,y),"size":0.25,"shape":"circle"})
    return cols
def _place_beams(w,d):
    return [{"start":(0,0.2),"end":(w,0.2),"width":0.2},{"start":(0,d-0.2),"end":(w,d-0.2),"width":0.2}]

def generate_design(building, modules, num_floors=2, n_rooms=4, enforce=True):
    total_area = 100 + modules*25
    floor_area = total_area/num_floors
    floors = []
    for lvl in range(1, num_floors+1):
        fl = create_floor(lvl, building, total_area, modules, floor_area, n_rooms, enforce)
        if fl: floors.append(fl)
    return {"id":str(uuid.uuid4())[:8].upper(),"building":building,"domain":get_domain(building),
            "modules":modules,"floors":floors,"area":total_area,"num_floors":num_floors,"cost":0,
            "structure":{"columns":sum(len(f["columns"]) for f in floors),
                         "beams":sum(len(f["beams"]) for f in floors)}}

# ---------- EVOLUTION ENGINE ----------
def mutate_design(design):
    child = json.loads(json.dumps(design))
    for floor in child["floors"]:
        if random.random() < 0.3:
            floor["columns"].append({"center":(random.uniform(1,5), random.uniform(1,5)), "size":0.25, "shape":"circle"})
        if random.random() < 0.3:
            floor["beams"].append({"start":(0, random.uniform(0.5,5)), "end":(random.uniform(4,8), random.uniform(0.5,5)), "width":0.2})
    child["cost"] = int(child["area"] * random.randint(1400, 2800))
    child["structure"] = {
        "columns": sum(len(f["columns"]) for f in child["floors"]),
        "beams": sum(len(f["beams"]) for f in child["floors"])
    }
    return child

def calculate_fitness(design):
    structural_ratio = design["structure"]["beams"] / max(1, design["structure"]["columns"])
    struct_score = max(0, 100 - int(abs(structural_ratio - 2.1) * 22))
    cost_per_sqm = design["cost"] / max(1, design["area"])
    cost_score = max(0, 100 - int(abs(cost_per_sqm - 1650) * 0.04))
    complexity_score = min(100, sum(len(f["rooms"]) for f in design["floors"]) * 9)
    return {"structural_integrity": struct_score, "cost_efficiency": cost_score, "spatial_complexity": complexity_score}

def aggregate_score(fitness):
    return int(sum(fitness.values()) / len(fitness))

def evolve_design(building, modules, num_floors, n_rooms, generations, pop_size, enforce):
    population = [generate_design(building, modules, num_floors, n_rooms, enforce) for _ in range(pop_size)]
    history = []
    for gen in range(generations):
        for d in population:
            d["fitness"] = calculate_fitness(d)
            d["score"] = aggregate_score(d["fitness"])
        population.sort(key=lambda x: x["score"], reverse=True)
        history.append(population[0]["score"])
        survivors = population[:max(2, pop_size//2)]
        next_pop = []
        for parent in survivors:
            next_pop.append(parent)
            next_pop.append(mutate_design(parent))
        population = next_pop[:pop_size]
    return population[0], history, population

# ---------- 2D FLOOR PLAN ----------
def draw_opening(draw, poly, opening, scale, tx_func, adjacent_name=None):
    wall = opening.get("wall","south"); wid = opening.get("width",0.9)
    if wall=="north": p1,p2 = poly[0],poly[1]
    elif wall=="south": p1,p2 = poly[3],poly[2]
    elif wall=="east": p1,p2 = poly[1],poly[2]
    else: p1,p2 = poly[0],poly[3]
    dx,dy = p2[0]-p1[0], p2[1]-p1[1]
    length = math.hypot(dx,dy)
    if length==0: return
    frac = 0.5 - (wid/length)/2
    if frac < 0: frac = 0
    sx = p1[0]+dx*frac; sy = p1[1]+dy*frac
    ex = sx+dx*(wid/length); ey = sy+dy*(wid/length)
    s = tx_func(sx,sy); e = tx_func(ex,ey)
    if opening["type"]=="door":
        draw.line([s,e], fill=(255,255,255), width=6)
        mid = ((s[0]+e[0])//2,(s[1]+e[1])//2)
        draw.arc([mid[0]-8,mid[1]-8,mid[0]+8,mid[1]+8],0,90,fill=(0,0,0))
        if adjacent_name:
            draw.text((mid[0]-10,mid[1]-15), adjacent_name, fill=(255,0,0), font=FONT)
    else:
        draw.line([s,e], fill=(255,255,255), width=6)
        draw.line([s,e], fill=(34,197,94), width=3)

def generate_floor_plan(design, floor_idx=0, scale=35, show_adjacency=True):
    if floor_idx>=len(design.get("floors",[])): return None
    floor = design["floors"][floor_idx]
    pts=[]
    for wall in floor["walls"]: pts.extend([wall["start"],wall["end"]])
    for col in floor["columns"]: pts.append(col["center"])
    if not pts: return None
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    min_x,max_x=min(xs),max(xs); min_y,max_y=min(ys),max(ys)
    margin=1.5
    wp=int((max_x-min_x+2*margin)*scale)+60; hp=int((max_y-min_y+2*margin)*scale)+60
    img=Image.new('RGB',(wp,hp),(245,245,245)); draw=ImageDraw.Draw(img)
    def tx(x,y): return ((x-min_x+margin)*scale+30,(y-min_y+margin)*scale+30)

    draw.rectangle([tx(min_x,min_y),tx(max_x,max_y)],outline=(150,150,150),width=2)
    for wall in floor["walls"]:
        p1,p2=tx(*wall["start"]),tx(*wall["end"])
        thick=max(2,int(wall.get("thickness",0.25)*scale))
        draw.line([p1,p2],fill=(40,40,40),width=thick)
    for col in floor["columns"]:
        c=tx(*col["center"]); size=max(2,int(col["size"]*scale))
        if col.get("shape")=="circle": draw.ellipse([c[0]-size,c[1]-size,c[0]+size,c[1]+size],fill=(100,100,100))
        else: draw.rectangle([c[0]-size,c[1]-size,c[0]+size,c[1]+size],fill=(100,100,100))
    for beam in floor["beams"]:
        p1,p2=tx(*beam["start"]),tx(*beam["end"]); draw.line([p1,p2],fill=(255,180,0),width=5)

    room_colors = {"living":(200,240,200),"kitchen":(255,245,200),"dining":(240,230,200),
                   "bedroom":(180,230,180),"bathroom":(210,190,230),"corridor":(235,240,235),
                   "office":(200,235,200),"meeting":(220,200,240),"reception":(190,220,190),
                   "hall":(210,210,190),"storage":(200,200,200),"study":(230,220,240)}
    for idx, room in enumerate(floor["rooms"]):
        poly = [tx(x,y) for (x,y) in room["polygon"]]
        color = room_colors.get(room.get("type",""),(210,230,210))
        draw.polygon(poly,fill=color,outline=(80,80,80))
        if poly:
            cx=sum(p[0] for p in poly)/len(poly); cy=sum(p[1] for p in poly)/len(poly)
            draw.text((cx-20,cy-5),room["name"][:10],fill=(0,0,0),font=FONT)
        for op in room.get("openings",[]):
            adj_text = None
            if show_adjacency and op["type"]=="door":
                adj = op.get("adjacent")
                if adj is not None and adj < len(floor["rooms"]):
                    adj_text = floor["rooms"][adj]["name"][:6]
            draw_opening(draw, room["polygon"], op, scale, tx, adj_text)
    draw.text((10,5),f"Floor {floor['level']} - {design.get('building','')}",fill=(20,20,20))
    buf=io.BytesIO(); img.save(buf,format="PNG"); return buf.getvalue()

# ---------- 3D STACKED VIEW ----------
def cuboid_mesh(x0,y0,z0,dx,dy,dz):
    x=[x0,x0+dx,x0+dx,x0,x0,x0+dx,x0+dx,x0]
    y=[y0,y0,y0+dy,y0+dy,y0,y0,y0+dy,y0+dy]
    z=[z0,z0,z0,z0,z0+dz,z0+dz,z0+dz,z0+dz]
    i=[0,0,4,4,0,1,5,4,1,2,6,5,2,3,7,6,3,0,4,7,1,0,3,2]
    j=[1,3,5,7,1,5,6,5,2,6,7,6,3,7,4,7,0,4,5,4,0,3,2,1]
    k=[3,2,7,6,4,4,5,5,6,5,6,6,7,6,7,7,7,5,4,4,3,2,1,0]
    return x,y,z,i,j,k
def cylinder_mesh(cx,cy,zb,zt,radius,n=12):
    theta=np.linspace(0,2*np.pi,n,endpoint=False)
    xb=cx+radius*np.cos(theta); yb=cy+radius*np.sin(theta)
    xt,yt=xb,yb; zb_arr=np.full_like(xb,zb); zt_arr=np.full_like(xt,zt)
    x=np.concatenate([xb,xt]); y=np.concatenate([yb,yt]); z=np.concatenate([zb_arr,zt_arr])
    i,j,k=[],[],[]
    for idx in range(n):
        nxt=(idx+1)%n
        i.extend([idx,nxt,n+nxt,n+idx]); j.extend([nxt,n+nxt,n+nxt,n+idx]); k.extend([n+nxt,n+idx,n+idx,nxt])
    return x,y,z,i,j,k
def build_3d_stacked_figure(design):
    fig=go.Figure()
    for fi,floor in enumerate(design["floors"]):
        z_base = fi*floor.get("height",3.0); z_top = z_base+floor.get("height",3.0)
        slab_thick = floor.get("slab",{}).get("thickness",0.2)
        all_x=[p[0] for wall in floor["walls"] for p in (wall["start"],wall["end"])]
        all_y=[p[1] for wall in floor["walls"] for p in (wall["start"],wall["end"])]
        min_x,max_x=min(all_x),max(all_x); min_y,max_y=min(all_y),max(all_y)
        x,y,z,i,j,k=cuboid_mesh(min_x,min_y,z_base,max_x-min_x,max_y-min_y,slab_thick)
        fig.add_trace(go.Mesh3d(x=x,y=y,z=z,i=i,j=j,k=k,color=f'hsl({fi*60},60%,50%)',opacity=0.3,name=f'Slab F{floor["level"]}'))
        for wall in floor["walls"]:
            sx,sy=wall["start"]; ex,ey=wall["end"]; dx=ex-sx; dy=ey-sy; length=np.sqrt(dx**2+dy**2); angle=np.arctan2(dy,dx)
            thick=wall.get("thickness",0.25)
            wx,wy,wz,iw,jw,kw=cuboid_mesh(sx,sy-thick/2,z_base,length,thick,z_top-z_base)
            wx,wy=np.array(wx)-sx,np.array(wy)-sy; cos_a,sin_a=np.cos(angle),np.sin(angle)
            rotx=wx*cos_a-wy*sin_a; roty=wx*sin_a+wy*cos_a; wx=rotx+sx; wy=roty+sy
            fig.add_trace(go.Mesh3d(x=wx,y=wy,z=wz,i=iw,j=jw,k=kw,color='tan',opacity=0.7,showlegend=False))
        for col in floor["columns"]:
            cx,cy=col["center"]; radius=col["size"]/2
            xc,yc,zc,ic,jc,kc=cylinder_mesh(cx,cy,z_base,z_top,radius)
            fig.add_trace(go.Mesh3d(x=xc,y=yc,z=zc,i=ic,j=jc,k=kc,color='grey',opacity=0.8,showlegend=False))
        beam_z_base=z_top-slab_thick-0.4
        for beam in floor["beams"]:
            sx,sy=beam["start"]; ex,ey=beam["end"]; dx=ex-sx; dy=ey-sy; length=np.sqrt(dx**2+dy**2); angle=np.arctan2(dy,dx)
            bw=beam.get("width",0.2); bh=0.4
            bx,by,bz,ib,jb,kb=cuboid_mesh(sx,sy-bw/2,beam_z_base,length,bw,bh)
            bx,by=np.array(bx)-sx,np.array(by)-sy; cos_a,sin_a=np.cos(angle),np.sin(angle)
            rotx=bx*cos_a-by*sin_a; roty=bx*sin_a+by*cos_a; bx=rotx+sx; by=roty+sy
            fig.add_trace(go.Mesh3d(x=bx,y=by,z=bz,i=ib,j=jb,k=kb,color='seagreen',opacity=0.6,showlegend=False))
        cx=(min_x+max_x)/2; cy=(min_y+max_y)/2
        fig.add_trace(go.Scatter3d(x=[cx],y=[cy],z=[z_top+0.2],mode='text',text=[f"Floor {floor['level']}"],
                                   textfont=dict(size=14,color='white'),showlegend=False))
    fig.update_layout(scene=dict(xaxis=dict(visible=False),yaxis=dict(visible=False),zaxis=dict(visible=False),
                                 aspectmode='data',camera=dict(eye=dict(x=1.5,y=1.5,z=1.2))),
                      margin=dict(l=0,r=0,t=30,b=0),height=600,title="3D Stacked View")
    return fig

# ---------- ELEVATIONS (ROBUST FIX) ----------
def generate_elevation(design, direction='south'):
    if not design.get("floors"):
        return None
    # gather all wall coordinates
    all_x, all_y = [], []
    for floor in design["floors"]:
        for wall in floor["walls"]:
            all_x.extend([wall["start"][0], wall["end"][0]])
            all_y.extend([wall["start"][1], wall["end"][1]])
    if not all_x:
        return None
    min_x, max_x = min(all_x), max(all_x)
    width = max_x - min_x
    if width <= 0:
        width = 1  # force a minimal width to avoid division by zero
    total_height = sum(f["height"] for f in design["floors"])
    if total_height <= 0:
        total_height = 3  # default height for a single floor

    scale = 30
    margin_px = 60
    img_w = max(100, int(width * scale) + margin_px)
    img_h = max(100, int(total_height * scale) + margin_px)

    img = Image.new('RGB', (img_w, img_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    def tx(x, y):
        # Convert building coordinates to image pixels
        px_x = int((x - min_x) * scale) + margin_px // 2
        px_y = int(img_h - y * scale - margin_px // 2)
        # Clamp to image bounds
        px_x = max(0, min(px_x, img_w - 1))
        px_y = max(0, min(px_y, img_h - 1))
        return (px_x, px_y)

    # Ensure rectangle coordinates are valid (top-left then bottom-right)
    top_left = tx(min_x, 0)
    bottom_right = tx(max_x, total_height)
    x1, y1 = top_left
    x2, y2 = bottom_right
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    if x2 - x1 > 0 and y2 - y1 > 0:
        draw.rectangle([(x1, y1), (x2, y2)], outline=(100, 100, 100), width=2)

    # draw openings
    for floor in design["floors"]:
        for room in floor["rooms"]:
            for op in room["openings"]:
                if (direction in ('north','south') and op["wall"] in ('north','south')) or \
                   (direction in ('east','west') and op["wall"] in ('east','west')):
                    poly = room["polygon"]
                    if direction in ('north','south'):
                        x1_wall, x2_wall = (poly[3][0], poly[2][0]) if direction == 'south' else (poly[0][0], poly[1][0])
                    else:
                        y_vals = [p[1] for p in poly]
                        x1_wall, x2_wall = min(y_vals), max(y_vals)
                    op_w = op["width"]
                    ox = (x1_wall + x2_wall) / 2 - op_w / 2
                    cum_z = (floor["level"] - 1) * floor["height"]
                    sill_y = cum_z + 1.0
                    ox = max(min_x, min(ox, max_x - op_w))
                    # Draw window/door opening as a small rectangle
                    top_left_op = tx(ox, sill_y)
                    bottom_right_op = tx(ox + op_w, sill_y + 1.2)
                    xo1, yo1 = top_left_op
                    xo2, yo2 = bottom_right_op
                    if xo1 > xo2:
                        xo1, xo2 = xo2, xo1
                    if yo1 > yo2:
                        yo1, yo2 = yo2, yo1
                    if xo2 - xo1 > 0 and yo2 - yo1 > 0:
                        draw.rectangle([(xo1, yo1), (xo2, yo2)], fill=(200, 230, 240), outline=(0, 0, 0))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# ---------- EXPORTS ----------
def export_ifc(design):
    return "ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION((''),'2;1');\nFILE_NAME('','',''),'RANDOM','');\nFILE_SCHEMA(('IFC2X3'));\nENDSEC;\nDATA;\nENDSEC;\nEND-ISO-10303-21;"
def design_to_glb(design):
    v=[0,0,0,1,0,0,0,1,0]; i=[0,1,2]
    vbin=struct.pack(f'<{len(v)}f',*v); ibin=struct.pack(f'<{len(i)}H',*i)
    try:
        from pygltflib import GLTF2, Buffer, BufferView, Accessor, Mesh, Primitive, Node, Scene, Asset, ELEMENT_ARRAY_BUFFER, ARRAY_BUFFER, FLOAT, UNSIGNED_SHORT
        gltf=GLTF2(); gltf.asset=Asset(version="2.0")
        buf=Buffer(byteLength=len(vbin)+len(ibin)); gltf.buffers.append(buf)
        bv1=BufferView(buffer=0,byteOffset=0,byteLength=len(vbin),target=ARRAY_BUFFER)
        bv2=BufferView(buffer=0,byteOffset=len(vbin),byteLength=len(ibin),target=ELEMENT_ARRAY_BUFFER)
        gltf.bufferViews.extend([bv1,bv2])
        acc1=Accessor(bufferView=0,byteOffset=0,componentType=FLOAT,count=len(v)//3,type="VEC3",max=[1,1,0],min=[0,0,0])
        acc2=Accessor(bufferView=1,byteOffset=0,componentType=UNSIGNED_SHORT,count=len(i),type="SCALAR",max=[2],min=[0])
        gltf.accessors.extend([acc1,acc2])
        prim=Primitive(attributes={"POSITION":0},indices=1); mesh=Mesh(primitives=[prim]); gltf.meshes.append(mesh)
        node=Node(mesh=0); gltf.nodes.append(node); scene=Scene(nodes=[0]); gltf.scenes.append(scene); gltf.scene=0
        gltf.binary_blob=vbin+ibin; return gltf.save_to_bytes()
    except: return None

# ---------- DIAGNOSTICS ----------
def structural_review(design):
    alerts = []
    cols = design["structure"]["columns"]
    beams = design["structure"]["beams"]
    if cols < 16:
        alerts.append("🔴 Column density too low for load transfer.")
    if design["cost"] / design["area"] > 2300:
        alerts.append("🟡 Cost efficiency threshold exceeded.")
    if beams / max(1, cols) < 1.9:
        alerts.append("🔵 Beam-column ratio imbalance.")
    return alerts if alerts else ["🟢 Design structurally stable."]

def material_takeoffs(design):
    cols = design["structure"]["columns"]
    beams = design["structure"]["beams"]
    area = design["area"]
    return [
        {"item": "High-Performance Concrete", "qty": f"{cols * 2.6:.1f} m³"},
        {"item": "Tensile Steel Rebar", "qty": f"{beams * 0.48:.2f} MT"},
        {"item": "CMU Blocks", "qty": f"{int(area * 42):,} units"},
        {"item": "Dead Load Base", "qty": f"{int(cols * 13.2):,} kN"}
    ]

# ---------- ROOM EDITOR ----------
def render_room_editor(design):
    if "floors" not in design: st.warning("No floors"); return
    floor_idx = st.selectbox("Floor", range(len(design["floors"])),
                             format_func=lambda i: f"Floor {design['floors'][i]['level']}")
    floor = design["floors"][floor_idx]
    room_names = [f"{r['name']} ({r['type']})" for r in floor["rooms"]]
    selected = st.selectbox("Select room", room_names)
    if selected is None: return
    room_idx = room_names.index(selected)
    room = floor["rooms"][room_idx]
    st.markdown("---")
    st.subheader(f"✏️ {room['name']}")
    col1,col2=st.columns(2)
    with col1:
        new_width = st.number_input("Width (m)",1.0,20.0,float(room["polygon"][1][0]-room["polygon"][0][0]))
    with col2:
        domain = get_domain(design["building"])
        rtypes = list(METRIC_STANDARDS[domain].keys())[:5]
        new_type = st.selectbox("Type", rtypes, index=rtypes.index(room["type"]) if room["type"] in rtypes else 0)
    col3,col4=st.columns(2)
    with col3:
        new_flooring = st.selectbox("Flooring", FLOORING_OPTS, index=FLOORING_OPTS.index(room.get("flooring","wood")) if room.get("flooring") in FLOORING_OPTS else 0)
    with col4:
        new_ceiling = st.selectbox("Ceiling", CEILING_OPTS, index=CEILING_OPTS.index(room.get("ceiling","flat")) if room.get("ceiling") in CEILING_OPTS else 0)
    st.markdown("#### Openings")
    openings = room.get("openings",[])
    for i,op in enumerate(openings):
        cols = st.columns([2,2,2,2,1])
        op_type = cols[0].selectbox("Type",["door","window"],index=0 if op["type"]=="door" else 1,key=f"optype_{i}")
        wall = cols[1].selectbox("Wall",["north","south","east","west"],
                                 index=["north","south","east","west"].index(op.get("wall","south")),key=f"opwall_{i}")
        width_val = cols[2].number_input("Width (m)",0.5,3.0,float(op.get("width",0.9)),0.1,key=f"opwidth_{i}")
        if op_type=="door":
            door_style = cols[0].selectbox("Style",["main","interior","bathroom"],
                                           index=["main","interior","bathroom"].index(op.get("door_type","interior")),
                                           key=f"opdoor_{i}")
            adj_options = [("None",None)] + [(f"{floor['rooms'][j]['name']}",j) for j in range(len(floor["rooms"])) if j!=room_idx]
            current_adj = op.get("adjacent")
            adj_idx = 0
            for k,(_,val) in enumerate(adj_options):
                if val==current_adj: adj_idx=k; break
            adj_choice = cols[3].selectbox("Connects to",[opt[0] for opt in adj_options],index=adj_idx,key=f"opadj_{i}")
            op["adjacent"] = adj_options[[opt[0] for opt in adj_options].index(adj_choice)][1]
        if cols[4].button("🗑",key=f"opdel_{i}"):
            openings.pop(i); st.rerun()
        op["type"]=op_type; op["wall"]=wall; op["width"]=width_val
    if st.button("➕ Add Opening"):
        openings.append({"type":"door","wall":"south","width":0.9,"door_type":"interior","adjacent":None})
        st.rerun()
    if st.button("💾 Apply Room Changes"):
        old_w = room["polygon"][1][0]-room["polygon"][0][0]; scale = new_width/old_w
        for i in range(len(room["polygon"])):
            x,y=room["polygon"][i]; room["polygon"][i]=(x*scale,y)
        room["type"]=new_type; room["flooring"]=new_flooring; room["ceiling"]=new_ceiling
        st.success("Room updated!")
    st.markdown("---")
    col_add,col_del=st.columns(2)
    with col_add:
        new_name = st.text_input("New room name")
        new_rt = st.selectbox("Type", rtypes, key="new_rt")
        if st.button("➕ Add Room") and new_name:
            last_x = floor["rooms"][-1]["polygon"][1][0] if floor["rooms"] else 0
            w=3.0; d=floor["walls"][2]["end"][1]
            poly=[(last_x,0),(last_x+w,0),(last_x+w,d),(last_x,d)]
            floor["rooms"].append({"name":new_name,"type":new_rt,"polygon":poly,"openings":[],"flooring":"wood","ceiling":"flat","ceiling_height":floor["height"]})
            st.rerun()
    with col_del:
        if st.button("🗑 Delete This Room") and len(floor["rooms"])>1:
            floor["rooms"].pop(room_idx); st.rerun()
    st.markdown("### Current Floor Plan")
    st.image(generate_floor_plan(design, floor_idx, show_adjacency=True), use_column_width=True)

# ============================================================
# SESSION INIT
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in=False; st.session_state.username=None
    st.session_state.user_data=None; st.session_state.memory=DEFAULT_MEMORY.copy()
    st.session_state.page="Random Copilot"; st.session_state.generated_concepts=[]
    st.session_state.unit_system="Metric"; st.session_state.evolved_population=[]

if not load_users():
    create_user("admin","admin123",role="admin")

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    col1,col2,col3=st.columns([1,2,1])
    with col2:
        st.markdown("<div class='logo-text' style='text-align:center;margin-top:4rem;'>⚡ RANDOM</div>",unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#94a3b8;'>AI Architectural Design Studio</p>",unsafe_allow_html=True)
        with st.form("auth"):
            uname=st.text_input("Username"); pw=st.text_input("Password",type="password")
            colA,colB=st.columns(2)
            with colA: login_btn=st.form_submit_button("Login")
            with colB: reg_btn=st.form_submit_button("Register")
            if login_btn:
                user=authenticate(uname,pw)
                if user:
                    st.session_state.logged_in=True; st.session_state.username=uname
                    st.session_state.user_data=user; st.session_state.memory=load_memory(uname)
                    st.rerun()
                else: st.error("Invalid credentials")
            if reg_btn:
                if not uname or not pw: st.error("Fill all fields")
                else:
                    try:
                        create_user(uname,pw); st.success("Account created!")
                    except ValueError as e: st.error(str(e))
    st.stop()

# ---------- SIDEBAR ----------
uname=st.session_state.username; user_data=st.session_state.user_data; memory=st.session_state.memory
with st.sidebar:
    st.markdown("<div class='logo-text' style='font-size:1.8rem;'>⚡ RANDOM</div>",unsafe_allow_html=True)
    st.markdown(f"**👤 {uname}**")
    lvl=user_data["level"]; xp=user_data["xp"]; needed=xp_for_level(lvl)
    progress=xp/needed if needed>0 else 1.0
    st.markdown(f"""<div class="xp-container"><span style="font-size:12px;color:#94a3b8;">LVL {lvl}</span>
    <div class="xp-bar-bg"><div class="xp-bar-fill" style="width:{progress*100}%;"></div></div>
    <span style="font-size:10px;color:#64748b;">{xp}/{needed} XP</span></div>""",unsafe_allow_html=True)
    page = st.radio("Go to",["Random Copilot","2D Plans","Room Editor","Sections & Elevations","3D Viewer",
                             "Reports","Diagnostics","Memory","Settings"])
    st.session_state.page=page
    st.divider()
    if user_data.get("role")=="admin":
        with st.expander("🛡️ Admin"):
            for u in load_users():
                if u["username"]!=uname:
                    if st.button(f"🗑 {u['username']}",key=f"del_{u['username']}"):
                        users=load_users(); users.remove(u); save_users(users); st.rerun()
    st.markdown("### 📁 Recent")
    for proj in memory["projects"][-5:]:
        st.markdown(f"• {proj['name']} *({proj['date']})*")
    if st.button("➕ New Project"):
        memory["projects"].append({"name":f"Project {len(memory['projects'])+1}","date":datetime.now().strftime("%b %d, %Y")})
        save_memory(uname,memory); st.rerun()
    if st.button("🚪 Logout"):
        save_memory(uname,memory)
        for k in ["logged_in","username","user_data","memory","generated_concepts","evolved_population"]:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

# ============================================================
# PAGE ROUTING
# ============================================================
page = st.session_state.page

if page == "Random Copilot":
    st.markdown("<div style='text-align:center;margin-bottom:2rem;'><h1>🧠 Random Copilot</h1><p style='color:#94a3b8;'>Generate or evolve optimal designs.</p></div>",unsafe_allow_html=True)
    cat = st.radio("Category",list(ARCH_TYPES.keys()),horizontal=True)
    bld = st.selectbox("Building Type",ARCH_TYPES[cat])
    col1,col2 = st.columns(2)
    with col1:
        floors = st.slider("Floors",1,10,2)
        rooms_per_floor = st.slider("Rooms per floor",1,8,4)
    with col2:
        modules = st.slider("Complexity (modules)",1,10,5)
    use_evolution = st.checkbox("Use evolutionary optimization", value=False)
    if use_evolution:
        generations = st.slider("Generations", 2, 30, 8)
        population = st.slider("Population", 4, 40, 12)
    enforce = st.checkbox("Use architectural standards",True)

    if st.button("⚡ Generate Design"):
        if not use_evolution:
            design = generate_design(bld, modules, floors, rooms_per_floor, enforce)
            st.session_state.generated_concepts = [design]
            st.session_state.evolved_population = []
        else:
            best, history, pop = evolve_design(bld, modules, floors, rooms_per_floor, generations, population, enforce)
            design = best
            st.session_state.generated_concepts = [design]
            st.session_state.evolved_population = pop
            st.line_chart(history)

        add_xp(uname,10); st.session_state.user_data=get_user(uname)
        memory["projects"].append({"name":design["building"],"date":datetime.now().strftime("%b %d, %Y")})
        save_memory(uname,memory)
        st.success(f"Design **{design['id']}** ready!")
        st.json({k:design[k] for k in ["id","building","area","num_floors","cost","score"] if k in design})

elif page == "2D Plans":
    if not st.session_state.generated_concepts: st.info("No design yet.")
    else:
        design = st.session_state.generated_concepts[0]
        if not design.get("floors"): st.info("No floors data.")
        else:
            floor_idx = st.slider("Floor",0,len(design["floors"])-1,0)
            img = generate_floor_plan(design, floor_idx, show_adjacency=True)
            if img: st.image(img, use_column_width=True)

elif page == "Room Editor":
    if not st.session_state.generated_concepts: st.info("No design yet.")
    else: render_room_editor(st.session_state.generated_concepts[0])

elif page == "Sections & Elevations":
    if not st.session_state.generated_concepts: st.info("No design yet.")
    else:
        design = st.session_state.generated_concepts[0]
        direction = st.selectbox("View",["north","south","east","west"])
        img = generate_elevation(design, direction)
        if img: st.image(img, caption=f"{direction.capitalize()} Elevation", use_column_width=True)

elif page == "3D Viewer":
    if not st.session_state.generated_concepts: st.info("No design yet.")
    else:
        design = st.session_state.generated_concepts[0]
        if design.get("floors"):
            fig = build_3d_stacked_figure(design)
            st.plotly_chart(fig, use_column_width=True)

elif page == "Reports":
    if not st.session_state.generated_concepts: st.info("No design yet.")
    else:
        design = st.session_state.generated_concepts[0]
        st.subheader(f"📄 {design['building']}")
        for floor in design["floors"]:
            with st.expander(f"Floor {floor['level']}"):
                for room in floor["rooms"]:
                    w = room["polygon"][1][0]-room["polygon"][0][0]; d = room["polygon"][3][1]-room["polygon"][0][1]
                    area = w*d
                    st.write(f"**{room['name']}** – {room['type']}, Area: {format_area(area,st.session_state.unit_system)}, Floor: {room.get('flooring','wood')}, Ceiling: {room.get('ceiling','flat')}")
        st.download_button("📥 Download JSON",json.dumps(design,indent=4),file_name=f"{design['id']}.json")
        if st.button("📐 Export IFC"): st.download_button("⬇️ IFC",export_ifc(design),file_name=f"{design['id']}.ifc")
        if st.button("🧊 Export glTF"):
            glb = design_to_glb(design)
            if glb: st.download_button("⬇️ GLB",glb,file_name=f"{design['id']}.glb")

elif page == "Diagnostics":
    st.markdown("## 🔍 Structural Diagnostics & Material Takeoffs")
    if not st.session_state.generated_concepts: st.info("No design loaded. Generate one first.")
    else:
        design = st.session_state.generated_concepts[0]
        st.subheader(f"Diagnostics for {design['building']} ({design['id']})")
        st.markdown("### Structural Review")
        for alert in structural_review(design):
            st.write(alert)
        st.markdown("### Material Quantity Estimates")
        df = pd.DataFrame(material_takeoffs(design))
        st.table(df)

elif page == "Memory":
    if not memory["saved_designs"]: st.info("No saved designs.")
    else:
        for i,saved in enumerate(memory["saved_designs"]):
            with st.expander(f"{saved.get('building','')} – {saved.get('id','')}"):
                st.json(saved)
                if st.button(f"Delete {saved['id']}",key=f"memdel_{i}"):
                    memory["saved_designs"].pop(i); save_memory(uname,memory); st.rerun()
    if st.session_state.generated_concepts:
        best = st.session_state.generated_concepts[0]
        if st.button(f"Save {best['id']} to Memory"):
            memory["saved_designs"].append(best); save_memory(uname,memory); st.success("Saved!")

elif page == "Settings":
    st.markdown("## ⚙️ Settings")
    unit = st.selectbox("Unit System",["Metric","Imperial","Dual"],index=0)
    st.session_state.unit_system = unit
    st.success("Settings updated.")

st.markdown('<div class="footer">AI Powered · Data Driven · Secure · Scalable</div>',unsafe_allow_html=True)
