import { Component } from "@angular/core";
import { FooterComponent } from "./components/footer/footer.component";
import { HeaderComponent } from "./components/header/header.component";

@Component({
  selector: "app-root",
  standalone: true,
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
  imports: [HeaderComponent, FooterComponent],
})
export class AppComponent {
  title = "frontend";
}
